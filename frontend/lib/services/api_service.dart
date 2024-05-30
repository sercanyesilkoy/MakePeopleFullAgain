import 'package:http/http.dart' as http;
import 'dart:convert';

// 에뮬레이터에서 실행할 경우
const String baseUrl = 'http://10.0.2.2:5000';

// 실제 디바이스에서 실행할 경우
// const String baseUrl = 'http://192.168.1.2:5000';  // 서버가 실행 중인 컴퓨터의 로컬 IP 주소로 변경하세요.

Future<Map<String, dynamic>> registerUser(String id, String name, int age, int income, String password) async {
  final response = await http.post(
    Uri.parse('$baseUrl/create_user'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, dynamic>{
      'id': id,
      'name': name,
      'age': age,
      'income': income,
      'password': password,
    }),
  );

  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Failed to register user');
  }
}

Future<Map<String, dynamic>> loginUser(String id, String password) async {
  final response = await http.post(
    Uri.parse('$baseUrl/login'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, dynamic>{
      'id': id,
      'password': password,
    }),
  );

  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Failed to login');
  }
}

Future<Map<String, dynamic>> resetDay() async {
  final response = await http.post(
    Uri.parse('$baseUrl/reset_day'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
  );

  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Failed to reset day');
  }
}
