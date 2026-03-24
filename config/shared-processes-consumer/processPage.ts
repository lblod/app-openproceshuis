import { logger } from '../logger';
import { updateSudo } from '@lblod/mu-auth-sudo';
import { sparqlEscapeUri } from 'mu';
import {
  BATCH_GRAPH,
  BYPASS_MU_AUTH,
  DIRECT_DATABASE_CONNECTION,
  TARGET_GRAPH,
  TIME_PREDICATE,
  VERSION_PREDICATE,
} from '../environment';
import { ConsumedInstances, consumedInstances } from './consumed-instances';

async function replaceExistingData(typeUri: string, filterString?: string) {
  let options = {};
  if (BYPASS_MU_AUTH) {
    options = {
      sparqlEndpoint: DIRECT_DATABASE_CONNECTION,
    };
  }
  await updateSudo(
    `
    DELETE {
      GRAPH ${sparqlEscapeUri(TARGET_GRAPH)} {
        ?s ?pOld ?oOld.
      }
    }
    INSERT {
      GRAPH ${sparqlEscapeUri(TARGET_GRAPH)} {
        ?s ?pNew ?oNew.
      }
    } WHERE {
      GRAPH ${sparqlEscapeUri(BATCH_GRAPH)} {
        ?stream <https://w3id.org/tree#member> ?versionedMember .
        ?versionMember a ${sparqlEscapeUri(typeUri)} .
        ?versionedMember ${sparqlEscapeUri(VERSION_PREDICATE)} ?s .
        ?versionedMember ?pNew ?oNew.
        FILTER (?pNew NOT IN ( ${sparqlEscapeUri(VERSION_PREDICATE)}, ${sparqlEscapeUri(TIME_PREDICATE)} ))
        ${filterString ?? ''}
      }
      OPTIONAL {
        GRAPH ${sparqlEscapeUri(TARGET_GRAPH)} {
          ?s ?pOld ?oOld.
        }
      }
    }`,
    {},
    options,
  );
}

export async function processPage() {
  logger.debug('Running custom logic to process the current page');
  const resources = Object.entries(consumedInstances) as [keyof ConsumedInstances, any][];
  for (const [typeUri, options] of resources) {
    const { filter } = options;
    logger.debug(`Getting resources in batch of type ${sparqlEscapeUri(typeUri)}`);
    logger.debug(`Applied filter for this resource type: \n ${filter ?? 'No filter added in config'}`)
    await replaceExistingData(typeUri, filter);
  }
  return;
}