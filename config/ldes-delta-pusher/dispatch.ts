import { moveTriples } from "../support";
import { Changeset, Quad, Term } from "../types";

import { querySudo } from "@lblod/mu-auth-sudo";
import { sparqlEscapeUri } from "mu";

import { ldesInstances } from './ldes-instances';
import { debug } from './logging';

export default async function dispatch(changesets: Changeset[]) {
	const inserts: Array<Quad> = [];
	changesets.map(changeset => inserts.push(...changeset.inserts));

	const publishQuads = await getQuadsForInterestingSubjects(inserts);
	debug('DISPATCH', `Will add ${publishQuads.length} quads to the stream.`)
	await moveTriples([
		{
			inserts: publishQuads,
			deletes: [],
		}
	]);
}

async function getQuadsForInterestingSubjects(arrayOfQuads: Array<Quad>): Promise<Array<Quad>> {
	const quadsToPublish: Array<Quad> = [];
	const uniqueSubjectUris = [...new Set(arrayOfQuads.map(q => q.subject.value))];
	debug('DISPATCH', `Found ${uniqueSubjectUris.length} subjects to check.`)
	for (const subjectUri of uniqueSubjectUris) {
		const typeSparqlResult = await querySudo(`
				SELECT DISTINCT ?type
				WHERE {
					${sparqlEscapeUri(subjectUri)} a ?type .

					FILTER(?type IN(${Object.keys(ldesInstances).map(type => sparqlEscapeUri(type)).join(',\n')}))
				}	LIMIT 1
			`)
		const typeUri = typeSparqlResult?.results?.bindings[0]?.['type']?.value;
		if (!Boolean(typeUri)) {
			debug('SUBJECT', `Not interested in type. (${typeUri})`)
			continue;
		}

		const typeFilter = ldesInstances[typeUri]?.filter;
		const ignoredPredicates = ldesInstances[typeUri]?.ignoredPredicates;
		let predicateFilter = '';
		if (ignoredPredicates && ignoredPredicates.length >= 1) {
			predicateFilter = `FILTER(?p NOT IN(${ignoredPredicates.map(uri => sparqlEscapeUri(uri)).join(',\n')}))`;
		}
		const sparqlResult = await querySudo(`
				SELECT DISTINCT ?s ?p ?o
				WHERE {
					?s a ${sparqlEscapeUri(typeUri)} .
					?s ?p ?o .
					${typeFilter}
					${predicateFilter}
					VALUES ?s { ${sparqlEscapeUri(subjectUri)} }
				}	
			`);
		quadsToPublish.push(...transformSparqlResultToArrayOfQuads(sparqlResult));
		debug('SUBJECT', `Fetched latest info for subject. (${subjectUri})`)
	}
	return quadsToPublish;
}

function transformSparqlResultToArrayOfQuads(sparqlResult: { results: { bindings: { s: Term; p: Term; o: Term; }[]; }; }): Array<Quad> {
	if (!Boolean(sparqlResult.results?.bindings)) {
		return []
	}

	return sparqlResult.results?.bindings.map((binding: { s: Term; p: Term; o: Term; }): Quad => {
		return {
			subject: binding.s,
			predicate: binding.p,
			object: binding.o,
		}
	})
}
