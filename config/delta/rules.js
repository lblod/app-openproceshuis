export default [
  {
    match: {
      subject: {},
    },
    callback: {
      url: "http://resource/.mu/delta",
      method: "POST",
    },
    options: {
      resourceFormat: "v0.0.1",
      gracePeriod: 250,
      ignoreFromSelf: true,
    },
  },
  {
    match: {
      // listen to all changes
    },
    callback: {
      url: "http://search/update",
      method: "POST",
    },
    options: {
      resourceFormat: "v0.0.1",
      gracePeriod: 1000,
      ignoreFromSelf: true,
    },
  },
];
