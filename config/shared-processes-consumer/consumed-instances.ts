export type ConsumedInstances = Record<string, { filter?: string }>;

export const consumedInstances = {
  "https://w3id.org/dpv#Process": {
    filter: `
      FILTER(?pNew != <http://mu.semte.ch/vocabularies/ext/hasStatistics>)
    `,
  },
  "http://lblod.data.gift/vocabularies/openproceshuis/ConceptueelProces": {
  },
  "http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#Bookmark": {},
  "http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#FileDataObject": {
    filter: `
      FILTER(?pNew IN (
        <http://www.semanticdesktop.org/ontologies/2007/01/19/nie#isPartOf>,
        <https://schema.org/associatedMedia>
      )) 
    `,
  },
  "http://lblod.data.gift/vocabularies/informationclassification/InformationAsset": {},
}