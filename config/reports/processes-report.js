import { generateReportFromData, batchedQuery } from "../helpers.js";

const reportName = "Alle processen";

export default {
  cronPattern: "0 3 * * *",
  name: reportName,
  execute: async () => {
    const reportInfo = {
      title: reportName,
      description: "Lijst van alle processen en hun besturen",
      filePrefix: "report-processes",
    };

    const queryString = `
      PREFIX besluit: <http://data.vlaanderen.be/ns/besluit#>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
      PREFIX proces: <https://data.vlaanderen.be/ns/proces#>
      PREFIX dct: <http://purl.org/dc/terms/>
      PREFIX adms: <http://www.w3.org/ns/adms#>

      SELECT DISTINCT *
      WHERE {
        ?group a besluit:Bestuurseenheid ;
               skos:prefLabel ?groupName .

        ?process a proces:Proces ;
                 dct:publisher ?group ;
                 dct:title ?title ;
                 dct:created ?created ;
                 dct:modified ?modified .

        OPTIONAL { ?process adms:status ?status }
      }
      ORDER BY LCASE(?groupName), LCASE(?title), ?created, ?modified, ?status
      `;
    const queryResponse = await batchedQuery(queryString);

    const data = queryResponse.results.bindings.map((process) => ({
      Bestuur: process.groupName.value,
      Proces: process.title.value,
      "Aangemaakt op": formatDate(process.created.value),
      "Aangepast op": formatDate(process.modified.value),
      Gearchiveerd:
        process.status?.value ===
        "http://lblod.data.gift/concepts/concept-status/gearchiveerd"
          ? "Ja"
          : "Nee",
    }));

    await generateReportFromData(
      data,
      ["Bestuur", "Proces", "Aangemaakt op", "Aangepast op", "Gearchiveerd"],
      reportInfo
    );
  },
};

function formatDate(isoString) {
  const date = new Date(isoString);

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");

  return `${year}-${month}-${day} ${hours}:${minutes}`;
}
