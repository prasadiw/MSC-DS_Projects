import java.io.IOException;

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

public class TablePartA{

   public static void main(String[] args) throws IOException {
      Configuration con = HBaseConfiguration.create();
      HBaseAdmin admin = new HBaseAdmin(con);

      HTableDescriptor powersDescriptor = new HTableDescriptor(TableName.valueOf("powers"));
      powersDescriptor.addFamily(new HColumnDescriptor("personal"));
      powersDescriptor.addFamily(new HColumnDescriptor("professional"));
      powersDescriptor.addFamily(new HColumnDescriptor("custom"));

      HTableDescriptor foodDescriptor = new HTableDescriptor(TableName.valueOf("food"));
      foodDescriptor.addFamily(new HColumnDescriptor("nutrition"));
      foodDescriptor.addFamily(new HColumnDescriptor("taste"));

      admin.createTable(powersDescriptor);
      admin.createTable(foodDescriptor);
   }
}

