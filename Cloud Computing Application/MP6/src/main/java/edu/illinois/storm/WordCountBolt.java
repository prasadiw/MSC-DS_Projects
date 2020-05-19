package edu.illinois.storm;

import org.apache.storm.topology.BasicOutputCollector;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseBasicBolt;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

/** a bolt that tracks word count */
public class WordCountBolt extends BaseBasicBolt {
  private static final Map<String, AtomicInteger> COUNTER_MAP = new HashMap<>();

  @Override
  public void execute(Tuple tuple, BasicOutputCollector collector) {
    String word = tuple.getStringByField("word");
    COUNTER_MAP.putIfAbsent(word, new AtomicInteger());
    AtomicInteger counter = COUNTER_MAP.get(word);
    collector.emit(new Values(word, counter.incrementAndGet()));
    System.out.println("Word: " + word + " Count : " + counter.get());
  }

  @Override
  public void declareOutputFields(OutputFieldsDeclarer declarer) {
    declarer.declare(new Fields("word", "count"));
  }
}
