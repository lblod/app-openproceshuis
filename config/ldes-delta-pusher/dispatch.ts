import { moveTriples } from "../support";
import { Changeset, Quad, Term } from "../types";
import { ldesInstances } from './ldes-instances';

import { querySudo } from "@lblod/mu-auth-sudo";
import { sparqlEscapeUri } from "mu";


export default async function dispatch(changesets: Changeset[]) {
	for (const changeset of changesets) {
		const typeFilterUnion = createTypeFilterUnion();
		const publishQuads = await getQuadsForInterestingSubjects(changeset.inserts, typeFilterUnion);

		await moveTriples([
			{
				inserts: publishQuads,
				deletes: [],
			}
		]);
	}
}

async function getQuadsForInterestingSubjects(arrayOfQuads: Array<Quad>, commonFilter: string): Promise<Array<Quad>> {
	const quadsToPublish: Array<Quad> = [];
	const uniqueSubjectUris = [...new Set(arrayOfQuads.map(q => q.subject.value))]
	for (const subjectUri of uniqueSubjectUris) {
		const typeSparqlResult = await querySudo(`
				SELECT DISTINCT ?type
				WHERE {
					${sparqlEscapeUri(subjectUri)} a ?type .

					FILTER(?type IN(${Object.keys(ldesInstances).map(type => sparqlEscapeUri(type)).join(',\n')}))

					${commonFilter}
				}	LIMIT 1
			`)
		const typeUri = typeSparqlResult?.results?.bindings[0]?.['type']?.value;
		if (!Boolean(typeUri)) {
			continue;
		}

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
					${predicateFilter}
					VALUES ?s { ${sparqlEscapeUri(subjectUri)} }
				}	
			`);
		quadsToPublish.push(...transformSparqlResultToArrayOfQuads(sparqlResult));
	}
	return quadsToPublish;
}

function createTypeFilterUnion() {
	return Object.keys(ldesInstances).map(type => {
		return `
			{
				FILTER(?type = ${sparqlEscapeUri(type)})
				${ldesInstances[type]?.filter ?? ''}
			}
		`
	}).join('\n UNION') // NOTE Expensive + even more when the filters grow
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