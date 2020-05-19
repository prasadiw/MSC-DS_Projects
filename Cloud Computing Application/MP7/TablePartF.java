import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

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

public class TablePartF{

   public static void main(String[] args) throws IOException {
	   Configuration con = HBaseConfiguration.create();
	   HTable table = new HTable(con, "powers");
	   Scan scan = new Scan();
	   scan.addFamily(Bytes.toBytes("custom"));
	   scan.addFamily(Bytes.toBytes("personal"));
	   scan.addFamily(Bytes.toBytes("professional"));
	   ResultScanner scanner = table.getScanner(scan);
	   List<String[]> heroes = new ArrayList<>();

	   for (Result result = scanner.next(); result != null; result = scanner.next()) {
	   	String[] hero = new String[3];
	   	hero[0] = Bytes.toString(result.getValue(Bytes.toBytes("professional"), Bytes.toBytes("name")));
	   	hero[1] = Bytes.toString(result.getValue(Bytes.toBytes("personal"), Bytes.toBytes("power")));
	   	hero[2] = Bytes.toString(result.getValue(Bytes.toBytes("custom"), Bytes.toBytes("color")));
	   	heroes.add(hero);
	   }

	   scanner.close();
	   table.close();

	   for (int i = 0; i < heroes.size(); i++) {
		   for (int j = 0; j < heroes.size(); j++) {
			   if (heroes.get(i)[2].equals(heroes.get(j)[2]) && !heroes.get(i)[0].equals(heroes.get(j)[0])) {
				   String name = heroes.get(i)[0];
				   String power = heroes.get(i)[1];
				   String color = heroes.get(i)[2];

				   String name1 = heroes.get(j)[0];
				   String power1 = heroes.get(j)[1];
				   System.out.println(name + ", " + power + ", " + name1 + ", " + power1 + ", "+color);
			   }
		   }
	   }

   }
}
