import Router from 'express-promise-router';

import { query } from 'mu';
import { Request, Response } from 'express';
import { Parser } from '@traqula/parser-sparql-1-1';

import { HttpError } from '../util/http-error';

export const sparqlRouter = Router();

sparqlRouter.post('/', async (req: Request, res: Response) => {
  const queryString = req.body.query ?? req.body.update;

  if (!queryString) {
    throw new HttpError(
      'No query value was found.',
      400,
      `The endpoint received a body without the property 'query' or 'body'.`,
      req.body
    );
  }

  const queryValidationResult = validateQuery(queryString)
  if (!queryValidationResult.isValid) {
    throw new HttpError(
      queryValidationResult.message,
      422,
      queryValidationResult.description,
    );
  }

  try {
    const result = await query(queryString);
    res.status(200).send(result);
  } catch (error) {
    throw new HttpError(
      'Something went wrong while executing the query.',
      500,
      `Check the d`,
      error
    );
  }
});

function validateQuery(queryString: string) {
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
      description: err.message,
      location: err.location
    };
  }
}

