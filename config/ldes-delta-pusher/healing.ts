import { ldesInstances } from './ldes-instances';

export type HealingConfig = Awaited<ReturnType<typeof getHealingConfig>>;
export const getHealingConfig = async () => {
  const entities: any = {};
  Object.keys(ldesInstances).map(typeUri => {
    if (ldesInstances[typeUri].healingPredicates) {
      entities[typeUri] = {
        healingPredicates: ldesInstances[typeUri].healingPredicates,
        instanceFilter: ldesInstances[typeUri].filter
      };
    }
  })

  return {
    public: {
      entities,
    }
  };
};
