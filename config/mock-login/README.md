# Mock accounts generation rules

Mock accounts are generated for each bestuur. Depending on `rules.json`, accounts get assigned certain roles. Which role(s) depends on the bestuur's classification.

## Rules regarding assignment of roles

### `Medewerker-fixed`

| Label     | Classification URI                                                                             |
| --------- | ---------------------------------------------------------------------------------------------- |
| Provincie | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/5ab0e9b8a3b2ca7c5e000000 |
| Gemeente  | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/5ab0e9b8a3b2ca7c5e000001 |
| OCMW      | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/5ab0e9b8a3b2ca7c5e000002 |
| District  | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/5ab0e9b8a3b2ca7c5e000003 |

### `OpenProcesHuis-Lezer`

| Label                                      | Classification URI                                                                                         |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| Agentschap Binnenlands Bestuur             | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/52cc9d8d-1c9a-4d92-9936-da9d4a622ec4 |
| Digitaal Vlaanderen                        | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/4d79a18a-7a46-4b03-8712-3bcf3467787b |
| Leverancier                                | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/c4483583-f9fe-4d2f-96f4-47ddb3440d71 |
| Vereniging van Vlaamse Steden en Gemeenten | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/fd4dda91-a6a5-485a-9d49-1378c94a5ff0 |
| Agentschap Facilitair Bedrijf              | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/548ce228-22ac-491f-9481-9dc31c8a5836 |

### `OpenProcesHuis-Procesbeheerder`

| Label                                      | Classification URI                                                                                         |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| Provincie                                  | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/5ab0e9b8a3b2ca7c5e000000             |
| Gemeente                                   | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/5ab0e9b8a3b2ca7c5e000001             |
| OCMW                                       | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/5ab0e9b8a3b2ca7c5e000002             |
| District                                   | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/5ab0e9b8a3b2ca7c5e000003             |
| Agentschap Binnenlands Bestuur             | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/52cc9d8d-1c9a-4d92-9936-da9d4a622ec4 |
| Digitaal Vlaanderen                        | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/4d79a18a-7a46-4b03-8712-3bcf3467787b |
| Leverancier                                | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/c4483583-f9fe-4d2f-96f4-47ddb3440d71 |
| Vereniging van Vlaamse Steden en Gemeenten | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/fd4dda91-a6a5-485a-9d49-1378c94a5ff0 |
| Agentschap Facilitair Bedrijf              | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/548ce228-22ac-491f-9481-9dc31c8a5836 |

### `LoketLB-admin`

| Label                          | Classification URI                                                                                         |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| Agentschap Binnenlands Bestuur | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/52cc9d8d-1c9a-4d92-9936-da9d4a622ec4 |
| Digitaal Vlaanderen            | http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/4d79a18a-7a46-4b03-8712-3bcf3467787b |