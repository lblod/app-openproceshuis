import { Quad } from "../types";

// NOTE easy but not the preferred way..
export function createTombstoneQuads(subjectUri: string, typeUri: string) {
  const values = [
    {
      predicate: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
      type: 'uri',
      object: 'http://www.w3.org/ns/activitystreams#Tombstone'
    },
    {
      predicate: 'http://purl.org/dc/terms/modified',
      type: 'typed-literal',
      datatype: 'http://www.w3.org/2001/XMLSchema#dateTime',
      object: new Date().toJSON()
    },
    {
      predicate: 'http://www.w3.org/ns/activitystreams#deleted',
      type: 'typed-literal',
      datatype: 'http://www.w3.org/2001/XMLSchema#dateTime',
      object: new Date().toJSON()
    },
    {
      predicate: 'http://www.w3.org/ns/activitystreams#formerType',
      type: 'uri',
      object: typeUri
    }
  ];

  return values.map(v => {
    const quad: Quad = {
      subject: {
        type: 'uri',
        value: subjectUri
      },
      predicate: {
        type: 'uri',
        value: v.predicate
      },
      object: {
        type: v.type,
        value: v.object
      },
    }

    if (v.datatype) {
      quad.object.datatype = v.datatype;
    }

    return quad;
  })
}