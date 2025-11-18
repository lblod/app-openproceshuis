export type LdesInstances = Record<string, { filter?: string }>;

export const ldesInstances: LdesInstances = {
  "https://w3id.org/dpv#Process": {
    filter: `
      FILTER NOT EXISTS {
        ?s <http://www.w3.org/ns/adms#status> <http://lblod.data.gift/concepts/concept-status/gearchiveerd> .
      }
    `
  },
  "http://lblod.data.gift/vocabularies/openproceshuis/ConceptueelProces": {
    filter: `
      FILTER NOT EXISTS {
        ?s <http://www.w3.org/ns/adms#status> <http://lblod.data.gift/concepts/concept-status/gearchiveerd> .
      }
    `
  },
  "http://www.w3.org/2004/02/skos/core#Concept": {
    filter: `
        FILTER NOT EXISTS {
          ?s <http://www.w3.org/ns/adms#status> <http://lblod.data.gift/concepts/concept-status/gearchiveerd> .
        }
        ?s <http://www.w3.org/2004/02/skos/core#inScheme> ?scheme .
        FILTER (?scheme IN(
            <http://lblod.data.gift/concept-schemes/21fba7d7-d0f5-4133-a108-626d0eb62298>, # process-category
            <http://lblod.data.gift/concept-schemes/a8108a43-44fa-4b08-9794-064941f00dc1>, # process-domain
            <http://lblod.data.gift/concept-schemes/324e775f-2a48-4daa-9de0-9f62ef8ab22e>, # process-group
            <http://lblod.data.gift/concept-schemes/4c0f0408-01b9-4902-9640-477b667bd086>  # information-asset
          )
        )
      `
  },
  "http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#FileDataObject": {
    filter: `
      ?uploadedProcess <http://www.semanticdesktop.org/ontologies/2007/01/19/nie#isPartOf> ?s .
      FILTER NOT EXISTS {
        ?s <http://www.w3.org/ns/adms#status> <http://lblod.data.gift/concepts/concept-status/gearchiveerd> .
      }
    `
  },
}