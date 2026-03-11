import Router from 'express-promise-router';

import { query } from 'mu';
import { Request, Response } from 'express';

export const sparqlRouter = Router();

sparqlRouter.post('/', async (req: Request, res: Response) => {
  try {
    const result = await query(req.body.query);
    res.status(200).send(result);

  } catch (error) {
    res.status(500).send(error);
  }
});

