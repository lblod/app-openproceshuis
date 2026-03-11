import Router from 'express-promise-router';

import { query } from 'mu';
import { Request, Response } from 'express';
import { Parser } from '@traqula/parser-sparql-1-1';

export const sparqlRouter = Router();

sparqlRouter.post('/', async (req: Request, res: Response) => {
  const queryValidationResult = validateQuery(req.body.query)
  if (!queryValidationResult.isValid) {
    res.status(422).send(queryValidationResult);
  }

  const result = await query(req.body.query);
  res.status(200).send(result);
});

function validateQuery(queryString) {
  if (!queryString) {
    // For some reason the query string is empty when passing on a delete query
    return {
      isValid: true,
    }
  }

  const parser = new Parser();

  try {
    const result = parser.parse(queryString);
    return {
      isValid: true,
      queryType: result.type
    };
  } catch (err: any) {
    return {
      isValid: false,
      message: "Invalid SPARQL Syntax",
      details: err.message,
      location: err.location
    };
  }
}

