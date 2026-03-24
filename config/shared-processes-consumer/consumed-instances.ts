export type ConsumedInstances = Record<string, { filter?: string }>;

export const consumedInstances = {
  "https://w3id.org/dpv#Process": {
    filter: `
      ?versionMember <http://purl.org/dc/terms/publisher> ?publisher .
      FILTER(?pNew NOT IN(
        <http://mu.semte.ch/vocabularies/ext/hasStatistics>
      )
    `,
  },
  "http://lblod.data.gift/vocabularies/openproceshuis/ConceptueelProces": {},
  "http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#Bookmark": {},
  "http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#FileDataObject": {
    filter: `
      ?resource <http://www.semanticdesktop.org/ontologies/2007/01/19/nie#isPartOf> ?s .
      ?resource <https://schema.org/associatedMedia> ?s .
    `,
  },
  "http://lblod.data.gift/vocabularies/informationclassification/InformationAsset": {},
}