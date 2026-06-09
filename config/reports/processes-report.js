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
      PREFIX oph: <http://lblod.data.gift/vocabularies/openproceshuis/>      

      SELECT  ?process 
              ?organizationLabel
              ?isBlueprint 
              ?title 
              ?created 
              (MAX(?modified) AS ?lastModified) 
              (SAMPLE(?status) AS ?status) 
              (MAX(?processViews) AS ?maxViews) 
              (MAX(?bpmnDownloads) AS ?maxBpmn) 
              (MAX(?visioDownloads) AS ?maxVisio) 
              (MAX(?pdfDownloads) AS ?maxPdf) 
              (MAX(?svgDownloads) AS ?maxSvg) 
              (MAX(?pngDownloads) AS ?maxPng) 
              (GROUP_CONCAT(DISTINCT ?adminUnitLabel; SEPARATOR="; ") AS ?adminUnitLabels)
      WHERE {
        ?group a besluit:Bestuurseenheid ;
        skos:prefLabel ?organizationLabel .

        graph <http://mu.semte.ch/graphs/shared> {
          ?process a dpv:Process .
          FILTER NOT EXISTS {
            ?process oph:isVersionedResource "true"^^<http://www.w3.org/2001/XMLSchema#boolean> .
          }

          ?process dct:publisher ?group .
          ?process dct:title ?title .
          ?process dct:created ?created .
          ?process dct:modified ?modified .
          OPTIONAL { ?process icr:isBlueprint ?isBlueprint }
        } 
        OPTIONAL { ?process adms:status ?status }
        OPTIONAL { 
          ?process ext:hasStatistics ?stats .
          OPTIONAL { ?stats ext:processViews ?processViews }
          OPTIONAL { ?stats ext:bpmnDownloads ?bpmnDownloads }
          OPTIONAL { ?stats ext:visioDownloads ?visioDownloads }
          OPTIONAL { ?stats ext:pngDownloads ?pngDownloads }
          OPTIONAL { ?stats ext:svgDownloads ?svgDownloads }
          OPTIONAL { ?stats ext:pdfDownloads ?pdfDownloads }
        }
        OPTIONAL {
          ?process icr:isRelevantForAdministrativeUnit ?adminUnit .
          OPTIONAL { ?adminUnit skos:prefLabel ?adminUnitLabel }
        }
      }
      GROUP BY ?process ?organizationLabel ?isBlueprint ?title ?created ?lastModified
      ORDER BY LCASE(?organizationLabel) LCASE(?title) ?created  
    `;
    const queryResponse = await batchedQuery(queryString);

    const data = queryResponse.results.bindings.map((process) => ({
      Uri: process.process.value,
      Proces: process.title.value,
      Bestuur: process.organizationLabel.value,
      "Aangemaakt op": formatDate(process.created.value),
      "Aangepast op": formatDate(process.lastModified.value),
      Gearchiveerd:
        process.status?.value ===
        "http://lblod.data.gift/concepts/concept-status/gearchiveerd"
          ? "Ja"
          : "Nee",
      Blauwdruk: process.isBlueprint?.value === "1" ? "Ja" : "Nee",
      "Relevant voor type bestuur": process.adminUnitLabels?.value || "",
      "Aantal weergaven": process.maxViews?.value,
      "Totaal aantal downloads": String(
        [
          process.maxBpmn,
          process.maxVisio,
          process.maxPdf,
          process.maxSvg,
          process.maxPng,
        ]
          .map((download) => Number(download?.value) || 0) // Convert SPARQL values to numbers -> sum them up -> return as string
          .reduce((accumulator, currentValue) => accumulator + currentValue, 0)
      ),
      "Aantal downloads (bpmn)": process.maxBpmn?.value || "0",
      "Aantal downloads (vsdx)": process.maxVisio?.value || "0",
      "Aantal downloads (pdf)": process.maxPdf?.value || "0",
      "Aantal downloads (svg)": process.maxSvg?.value || "0",
      "Aantal downloads (png)": process.maxPng?.value || "0",
    }));

    await generateReportFromData(
      data,
      [
        "Uri",
        "Proces",
        "Bestuur",
        "Aangemaakt op",
        "Aangepast op",
        "Blauwdruk",
        "Gearchiveerd",
        "Relevant voor type bestuur",
        "Aantal weergaven",
        "Totaal aantal downloads",
        "Aantal downloads (bpmn)",
        "Aantal downloads (vsdx)",
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
