import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

class OnboardingVehiclePage extends StatefulWidget {
  const OnboardingVehiclePage({super.key, required this.onNext});
  final Future<void> Function() onNext;

  @override
  State<OnboardingVehiclePage> createState() => _OnboardingVehiclePageState();
}

class _OnboardingVehiclePageState extends State<OnboardingVehiclePage> {
  final _make = TextEditingController();
  final _model = TextEditingController();
  final _plate = TextEditingController();
  final _height = TextEditingController();
  String _powertrain = 'ICE';
  final _years = TextEditingController();
  bool _loading = false;
  String? _error;

  SupabaseClient get _sb => Supabase.instance.client;

  Future<void> _save() async {
    setState(() { _loading = true; _error = null; });
    try {
      final session = _sb.auth.currentSession;
      final authUser = session?.user;
      if (authUser == null) throw Exception('로그인이 필요합니다');
      final userRow = await _sb.from('users').select('id').eq('auth_user_id', authUser.id).maybeSingle();
      if (userRow == null) throw Exception('사용자 프로필이 필요합니다');
      await _sb.from('vehicles').insert({
        'user_id': userRow['id'],
        'make': _make.text.trim(),
        'model': _model.text.trim(),
        'plate_number': _plate.text.trim(),
        'powertrain': _powertrain,
        'height_m': double.tryParse(_height.text),
      });
      // store driving years to users
      final years = int.tryParse(_years.text);
      if (years != null) {
        await _sb.from('users').update({'driving_years': years}).eq('id', userRow['id']);
      }
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
          const Text('추가 정보', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          TextField(controller: _years, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: '운전 경력(년)')),
          const SizedBox(height: 12),
          TextField(controller: _make, decoration: const InputDecoration(labelText: '제조사')),
          const SizedBox(height: 12),
          TextField(controller: _model, decoration: const InputDecoration(labelText: '차종')),
          const SizedBox(height: 12),
          TextField(controller: _plate, decoration: const InputDecoration(labelText: '차량 번호판')),
          const SizedBox(height: 12),
          DropdownButton<String>(
            value: _powertrain,
            items: const [
              DropdownMenuItem(value: 'ICE', child: Text('내연기관')),
              DropdownMenuItem(value: 'EV', child: Text('전기차')),
            ],
            onChanged: (v) => setState(() => _powertrain = v ?? 'ICE'),
          ),
          const SizedBox(height: 12),
          TextField(controller: _height, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: '차량 높이(m)')),
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
