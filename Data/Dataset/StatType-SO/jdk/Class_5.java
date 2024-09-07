/*
 Date: 1/19/17
 URL: http://stackoverflow.com/questions/109383/sort-a-mapkey-value-by-values-java
 */


public class Class_5 {
	public static <K, V extends Comparable<? super V>> Map<K, V> sortByValue(Map<K, V> map) {
		List<Map.Entry<K, V>> list = new LinkedList<Map.Entry<K, V>>(map.entrySet());
		Collections.sort(list, new Comparator<Map.Entry<K, V>>() {
			public int compare(Map.Entry<K, V> o1, Map.Entry<K, V> o2) {
				return (o1.getValue()).compareTo(o2.getValue());
			}
		});

		Map<K, V> result = new LinkedHashMap<K, V>();
		for (Map.Entry<K, V> entry : list) {
			result.put(entry.getKey(), entry.getValue());
		}
		return result;
	}

	public class main {
		public void main_1() {
			HashMap<String, Double> map = new HashMap<String, Double>();
			ValueComparator bvc = new ValueComparator(map);
			TreeMap<String, Double> sorted_map = new TreeMap<String, Double>(bvc);

			map.put("A", 99.5);
			map.put("B", 67.4);
			map.put("C", 67.4);
			map.put("D", 67.3);

			System.out.println("unsorted map: " + map);
			sorted_map.putAll(map);
			System.out.println("results: " + sorted_map);
		}
	}

	class ValueComparator implements Comparator<String> {
		Map<String, Double> base;

		public ValueComparator(Map<String, Double> base) {
			this.base = base;
		}

		// Note: this comparator imposes orderings that are inconsistent with
		// equals.
		public int compare(String a, String b) {
			if (base.get(a) >= base.get(b)) {
				return -1;
			} else {
				return 1;
			} // returning 0 would merge keys
		}
	}

}