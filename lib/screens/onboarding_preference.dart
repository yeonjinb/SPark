import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

class OnboardingPreferencePage extends StatefulWidget {
  const OnboardingPreferencePage({super.key, required this.onFinish});
  final Future<void> Function() onFinish;

  @override
  State<OnboardingPreferencePage> createState() => _OnboardingPreferencePageState();
}

class _OnboardingPreferencePageState extends State<OnboardingPreferencePage> {
  int _price = 40;
  int _distance = 60;
  int _difficulty = 0;
  bool _loading = false;
  String? _error;

  SupabaseClient get _sb => Supabase.instance.client;

  Future<void> _save() async {
    setState(() { _loading = true; _error = null; });
    try {
      final authUser = _sb.auth.currentUser;
      if (authUser == null) throw Exception('로그인이 필요합니다');
      final userRow = await _sb.from('users').select('id').eq('auth_user_id', authUser.id).maybeSingle();
      if (userRow == null) throw Exception('사용자 프로필이 필요합니다');
      await _sb.from('user_settings').upsert({
        'user_id': userRow['id'],
        'weight_price': _price,
        'weight_distance': _distance,
        'weight_difficulty': _difficulty,
      }, onConflict: 'user_id');
      await widget.onFinish();
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
          const Text('선호 옵션', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          const Text('주차 비용 가중치'),
          Slider(value: _price.toDouble(), min: 0, max: 100, divisions: 20, label: '$_price', onChanged: (v) => setState(() => _price = v.toInt())),
          const SizedBox(height: 12),
          const Text('이동 거리 가중치'),
          Slider(value: _distance.toDouble(), min: 0, max: 100, divisions: 20, label: '$_distance', onChanged: (v) => setState(() => _distance = v.toInt())),
          const SizedBox(height: 12),
          const Text('운전 난이도 가중치'),
          Slider(value: _difficulty.toDouble(), min: 0, max: 100, divisions: 20, label: '$_difficulty', onChanged: (v) => setState(() => _difficulty = v.toInt())),
          if (_error != null) Text(_error!, style: const TextStyle(color: Colors.red)),
          const Spacer(),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _loading ? null : _save,
              child: _loading ? const SizedBox(height: 16, width: 16, child: CircularProgressIndicator(strokeWidth: 2)) : const Text('완료'),
            ),
          ),
        ],
      ),
    );
  }
}
