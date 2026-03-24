import { Changeset } from "../types";

export const interestingTypes = [
  "https://w3id.org/dpv#Process",
  "http://lblod.data.gift/vocabularies/openproceshuis/ConceptueelProces",
  "http://www.w3.org/2004/02/skos/core#Concept",
  "http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#FileDataObject",
  "http://www.w3.org/ns/activitystreams#Tombstone",
];

export const filterModifiedSubjects = "";

export async function filterDeltas(changeSets: Changeset[]) {
  const modifiedPred = "http://purl.org/dc/terms/modified";
  const subjectsWithModified = new Set();

  const trackModifiedSubjects = (quad) => {
    if (quad.predicate.value === modifiedPred) {
      subjectsWithModified.add(quad.subject.value);
    }
  };
  changeSets.map((changeSet) => {
    changeSet.inserts.forEach(trackModifiedSubjects);
  });

  const ignoredGraphPrefixes = [
    "http://mu.semte.ch/graphs/op/landing",
  ];
  const isGoodQuad = (quad) =>
    !subjectsWithModified.has(quad.subject.value) &&
    !ignoredGraphPrefixes.some((prefix) => quad.graph.value.startsWith(prefix));
  return changeSets.map((changeSet) => {
    return {
      inserts: changeSet.inserts.filter(isGoodQuad),
      deletes: changeSet.deletes.filter(isGoodQuad),
    };
  });
}
