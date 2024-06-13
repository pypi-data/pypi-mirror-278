import 'dart:io';
import 'kodik.dart';

void main() {
  final String bookPage = File('animego.html').readAsStringSync();
  Map<String, dynamic> result = KodikPage(bookPage).parse();
  for (var z in result.entries) {
    print(z.key);
    print("    ${z.value}");
  }
}
