import java.io.*;

import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;

import org.apache.hadoop.hbase.TableName;

import org.apache.hadoop.hbase.client.HBaseAdmin;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;

import org.apache.hadoop.hbase.util.Bytes;

public class TablePartC{

   public static void main(String[] args) throws IOException {
      Configuration con = HBaseConfiguration.create();
      HTable table = new HTable(con, "powers");

      BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream("input.csv")));
      while(reader.ready()) {
         String[] tokens = reader.readLine().split(",");
         Put p = new Put(Bytes.toBytes(tokens[0]));
         p.add(Bytes.toBytes("personal"), Bytes.toBytes("hero"), Bytes.toBytes(tokens[1]));
         p.add(Bytes.toBytes("personal"), Bytes.toBytes("power"), Bytes.toBytes(tokens[2]));
         p.add(Bytes.toBytes("professional"), Bytes.toBytes("name"), Bytes.toBytes(tokens[3]));
         p.add(Bytes.toBytes("professional"), Bytes.toBytes("xp"), Bytes.toBytes(tokens[4]));
         p.add(Bytes.toBytes("custom"), Bytes.toBytes("color"), Bytes.toBytes(tokens[5]));
         table.put(p);
      }
      table.close();
   }
}

