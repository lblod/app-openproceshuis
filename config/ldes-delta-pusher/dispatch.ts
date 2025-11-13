import { moveTriples } from "../support";
import { Changeset, Quad } from "../types";
import { ldesInstances } from './ldes-instances';

import { querySudo } from "@lblod/mu-auth-sudo";
import { sparqlEscapeUri } from "mu";


export default async function dispatch(changesets: Changeset[]) {
	const interestingSubjectUris: Array<string> = [];
	for (const changeset of changesets) {
		const interestingChanges = async (arrayOfQuads: Array<Quad>) => {
			const interestingQuads = [];
			for (const quad of arrayOfQuads) {
				const subjectUri = quad.subject.value;
				if (interestingSubjectUris.find(uri => uri === subjectUri)) {
					interestingQuads.push(quad);
				} else {
					const askIfInteresting = await querySudo(`
					ASK {
						${sparqlEscapeUri(subjectUri)} a ?type .

						VALUES ?type {
							${Object.keys(ldesInstances).map(type => sparqlEscapeUri(type)).join('\n')}
						}
					}	
				`);
					if (Boolean(askIfInteresting?.boolean)) {
						interestingSubjectUris.push(subjectUri);
						interestingQuads.push(quad);
					}
				}
			}
			return interestingQuads;
		}

		await moveTriples([
			{
				inserts: await interestingChanges(changeset.inserts),
				deletes: await interestingChanges(changeset.deletes),
			},
		]);
	}
}