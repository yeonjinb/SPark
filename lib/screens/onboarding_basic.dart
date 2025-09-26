import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

class OnboardingBasicPage extends StatefulWidget {
  const OnboardingBasicPage({super.key, required this.onNext});
  final Future<void> Function() onNext;

  @override
  State<OnboardingBasicPage> createState() => _OnboardingBasicPageState();
}

class _OnboardingBasicPageState extends State<OnboardingBasicPage> {
  final _name = TextEditingController();
  final _age = TextEditingController();
  bool _agreeLocation = false;
  bool _loading = false;
  String? _error;

  SupabaseClient get _sb => Supabase.instance.client;

  Future<void> _save() async {
    setState(() { _loading = true; _error = null; });
    try {
      final user = _sb.auth.currentUser;
      if (user == null) throw Exception('로그인이 필요합니다');
      // upsert users by auth_user_id
      await _sb.from('users').upsert({
        'auth_user_id': user.id,
        'name': _name.text.trim(),
        'age': int.tryParse(_age.text) ?? null,
      }, onConflict: 'auth_user_id');
      await widget.onNext();
    } catch (e) {
      setState(() { _error = e.toString(); });
    } finally {
      setState(() { _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('기본 정보', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          TextField(controller: _name, decoration: const InputDecoration(labelText: '이름')),
          const SizedBox(height: 12),
          TextField(controller: _age, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: '나이')),
          const SizedBox(height: 12),
          CheckboxListTile(
            value: _agreeLocation,
            onChanged: (v) => setState(() => _agreeLocation = v ?? false),
            title: const Text('위치 정보 제공에 동의합니다'),
          ),
          if (_error != null) Text(_error!, style: const TextStyle(color: Colors.red)),
          const Spacer(),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _loading ? null : _save,
              child: _loading ? const SizedBox(height: 16, width: 16, child: CircularProgressIndicator(strokeWidth: 2)) : const Text('다음'),
            ),
          ),
        ],
      ),
    );
  }
}
