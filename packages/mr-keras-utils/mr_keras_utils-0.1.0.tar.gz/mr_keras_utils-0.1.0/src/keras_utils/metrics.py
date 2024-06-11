import keras
from keras import ops

class MetricEveryN(keras.metrics.Metric):
  """A metric that only runs every `n` batches"""
  def __init__(self, metric_fn, name='custom_metric', n=10, **kwargs):
    super().__init__(name=name, **kwargs)
    self.metric_fn = metric_fn
    self.n = n
    self.total = self.add_weight(name='total', initializer='zeros')
    self.count = self.add_weight(name='count', initializer='zeros')
    self.batch_counter = self.add_weight(name='batch_counter', initializer='zeros')

  def update_state(self, y_true, y_pred, sample_weight=None):
    self.batch_counter.assign_add(1)

    # Only compute the metric every N batches
    result = ops.cond(
      ops.equal(self.batch_counter % self.n, 0),
      lambda: ops.mean(self.metric_fn(y_true, y_pred)),
      lambda: 0.0
    )
    count = ops.cond(
      ops.equal(self.batch_counter % self.n, 0),
      lambda: 1, lambda: 0
    )
    self.total.assign_add(result)
    self.count.assign_add(count)

  def result(self):
    return ops.cond(
      ops.equal(self.count, 0),
      lambda: 0.0,
      lambda: self.total / self.count
    )

  def reset_states(self):
    self.total.assign(0.0)
    self.count.assign(0.0)
    self.batch_counter.assign(0.0)
