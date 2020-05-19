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

public class TablePartE{

   public static void main(String[] args) throws IOException {
	   Configuration con = HBaseConfiguration.create();
	   HTable table = new HTable(con, "powers");
	   Scan scan = new Scan();
	   scan.addFamily(Bytes.toBytes("custom"));
	   scan.addFamily(Bytes.toBytes("personal"));
	   scan.addFamily(Bytes.toBytes("professional"));
	   ResultScanner scanner = table.getScanner(scan);

	   for (Result result = scanner.next(); result != null; result = scanner.next()) {
	   		System.out.println(result);
	   }

	   scanner.close();
	   table.close();
   }
}

