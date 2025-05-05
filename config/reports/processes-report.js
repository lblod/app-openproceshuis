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
      PREFIX dpv: <https://w3id.org/dpv#>
      PREFIX dct: <http://purl.org/dc/terms/>
      PREFIX adms: <http://www.w3.org/ns/adms#>
      PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>
      PREFIX icr: <http://lblod.data.gift/vocabularies/informationclassification/>

      SELECT DISTINCT ?groupName ?title ?created ?modified ?status ?processViews ?bpmnDownloads ?pdfDownloads ?svgDownloads ?pngDownloads (GROUP_CONCAT(DISTINCT ?adminUnitLabel; SEPARATOR="; ") AS ?adminUnitLabels)
      WHERE {
        ?group a besluit:Bestuurseenheid ;
               skos:prefLabel ?groupName .

        ?process a dpv:Process ;
                 dct:publisher ?group ;
                 dct:title ?title ;
                 dct:created ?created ;
                 dct:modified ?modified .
                 
        OPTIONAL { ?process adms:status ?status }
        OPTIONAL { 
          ?process ext:hasStatistics ?stats .
          OPTIONAL { ?stats ext:processViews ?processViews }
          OPTIONAL { ?stats ext:bpmnDownloads ?bpmnDownloads }
          OPTIONAL { ?stats ext:pngDownloads ?pngDownloads }
          OPTIONAL { ?stats ext:svgDownloads ?svgDownloads }
          OPTIONAL { ?stats ext:pdfDownloads ?pdfDownloads }
        }
          OPTIONAL {
                     ?process icr:isRelevantForAdministrativeUnit ?adminUnit .
          OPTIONAL { ?adminUnit skos:prefLabel ?adminUnitLabel }
        }

}
      GROUP BY ?groupName ?title ?created ?modified ?status ?processViews ?bpmnDownloads ?pdfDownloads ?svgDownloads ?pngDownloads
      ORDER BY LCASE(?groupName) LCASE(?title) ?created
       
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
      "Relevant voor type bestuur": process.adminUnitLabels?.value || "",
      "Aantal weergaven": process.processViews?.value,
      "Totaal aantal downloads": String(
        [
          process.bpmnDownloads,
          process.pdfDownloads,
          process.svgDownloads,
          process.pngDownloads,
        ]
          .map((download) => Number(download?.value) || 0) // Convert SPARQL values to numbers -> sum them up -> return as string
          .reduce((accumulator, currentValue) => accumulator + currentValue, 0)
      ),
      "Aantal downloads (bpmn)": process.bpmnDownloads?.value || "0",
      "Aantal downloads (pdf)": process.pdfDownloads?.value || "0",
      "Aantal downloads (svg)": process.svgDownloads?.value || "0",
      "Aantal downloads (png)": process.pngDownloads?.value || "0",
    }));

    await generateReportFromData(
      data,
      [
        "Bestuur",
        "Proces",
        "Aangemaakt op",
        "Aangepast op",
        "Gearchiveerd",
        "Relevant voor type bestuur",
        "Aantal weergaven",
        "Totaal aantal downloads",
        "Aantal downloads (bpmn)",
        "Aantal downloads (pdf)",
        "Aantal downloads (svg)",
        "Aantal downloads (png)",
      ],
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
