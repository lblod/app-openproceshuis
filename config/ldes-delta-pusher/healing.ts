export type HealingConfig = Awaited<ReturnType<typeof getHealingConfig>>;
export const getHealingConfig = async () => {
  return {
    public: {
      entities: {
        "https://w3id.org/dpv#Process": [
          "http://purl.org/dc/terms/modified",
        ],
        "http://lblod.data.gift/vocabularies/openproceshuis/ConceptueelProces": [
          "http://purl.org/dc/terms/modified",
        ],
        "http://www.w3.org/2004/02/skos/core#Concept": [
          "http://purl.org/dc/terms/modified",
        ],
        "http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#FileDataObject": [
          "http://purl.org/dc/terms/modified",
        ],
      },
    },
  };
};