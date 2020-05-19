package edu.illinois.storm;

import java.io.Serializable;
import java.util.Map.Entry;
import java.util.*;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

/** a bolt that finds the top n words. */
public class TopNFinderBolt extends BaseRichBolt {
  private OutputCollector collector;

  // Hint: Add necessary instance variables and inner classes if needed
  private int maximumSize;
  private PriorityQueue<Pair<Integer, String>> priorityQueue;
  private Map<String, Pair<Integer, String>> map;


  @Override
  public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
    this.collector = collector;
  }

  public TopNFinderBolt withNProperties(int N) {
    maximumSize = N;
    priorityQueue = new PriorityQueue<>(new PairComparator());
    map = new HashMap<>();
    return this;
  }

  @Override
  public void execute(Tuple tuple) {
    int count = tuple.getIntegerByField("count");
    String word = tuple.getStringByField("word");
    Pair<Integer, String> element = map.getOrDefault(word, null);
    if (priorityQueue.contains(element) || priorityQueue.size() < maximumSize) {
      if (element != null) {
        priorityQueue.remove(map.get(word));
      }
      element = new Pair<>(count, word);
      priorityQueue.add(element);
      map.put(word, element);
    } else if (count > priorityQueue.peek().getA()) {
      map.remove(priorityQueue.poll().getB());
      element = new Pair<>(count, word);
      priorityQueue.add(element);
      map.put(word, element);
    }
    StringBuffer sb = new StringBuffer();
    priorityQueue.stream().forEach(pair -> sb.append(pair.getB() + ", "));
    sb.setLength(sb.length()-2);
    collector.emit(new Values("top-N", sb.toString()));
  }

  @Override
  public void declareOutputFields(OutputFieldsDeclarer declarer) {
    declarer.declare(new Fields("top-N", "top-N-words"));
  }
}

class Pair<A, B> {
  private A a;
  private B b;

  Pair(A a, B b) {
    this.a = a;
    this.b = b;
  }

  public A getA() {
    return a;
  }

  public B getB() {
    return b;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Pair<?, ?> pair = (Pair<?, ?>) o;
    return b.equals(pair.b);
  }

  @Override
  public int hashCode() {
    return Objects.hash(b);
  }
}

class PairComparator implements Serializable, Comparator<Pair<Integer, String>> {
  @Override
  public int compare(Pair<Integer, String> t1, Pair<Integer, String> t2) {
    return t1.getA().compareTo(t2.getA());
  }
}

class EntryComparator implements Comparator<Entry<String, Integer>> {
  @Override
  public int compare(Entry<String, Integer> t1, Entry<String, Integer> t2) {
    return t2.getValue().compareTo(t1.getValue());
  }
}