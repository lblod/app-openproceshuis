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
      subject: {},
    },
    callback: {
      url: "http://modified/delta",
      method: "POST",
    },
    options: {
      resourceFormat: "v0.0.1",
      gracePeriod: 10000,
      retry: 3,
      ignoreFromSelf: true,
      retryTimeout: 250,
    },
  },
  {
    match: {
      subject: {},
    },
    callback: {
      url: "http://ldes-delta-pusher/publish",
      method: "POST",
    },
    options: {
      resourceFormat: "v0.0.1",
      ignoreFromSelf: false,
      gracePeriod: 15000,
    },
  },
];
