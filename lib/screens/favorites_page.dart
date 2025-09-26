import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../services/favorites.dart';

class FavoritesPage extends StatefulWidget {
  const FavoritesPage({super.key});

  @override
  State<FavoritesPage> createState() => _FavoritesPageState();
}

class _FavoritesPageState extends State<FavoritesPage> {
  late final FavoritesService _fav;
  bool _loading = true;
  String? _error;
  List<Map<String, dynamic>> _lots = [];

  @override
  void initState() {
    super.initState();
    _fav = FavoritesService(Supabase.instance.client);
    _load();
  }

  Future<void> _load() async {
    setState(() { _loading = true; _error = null; });
    try {
      final rows = await _fav.fetchFavoriteLots();
      setState(() { _lots = rows; });
    } catch (e) {
      setState(() { _error = e.toString(); });
    } finally {
      setState(() { _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('즐겨찾기')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(child: Text('오류: $_error'))
              : ListView.builder(
                  itemCount: _lots.length,
                  itemBuilder: (context, i) {
                    final lot = _lots[i];
                    return ListTile(
                      title: Text(lot['name']?.toString() ?? '주차장'),
                      subtitle: Text('요금 ${lot['price_per_hour']}원/시간 • EV ${lot['ev_charging'] == true ? '가능' : '불가'}'),
                    );
                  },
                ),
    );
  }
}
