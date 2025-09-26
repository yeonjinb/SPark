import 'package:supabase_flutter/supabase_flutter.dart';

class FavoritesService {
  FavoritesService(this._sb);
  final SupabaseClient _sb;

  Future<String?> _getUserRowId() async {
    final authUser = _sb.auth.currentUser;
    if (authUser == null) return null;
    final res = await _sb.from('users').select('id').eq('auth_user_id', authUser.id).limit(1);
    if (res.isEmpty) return null;
    return (res.first as Map)['id'] as String?;
  }

  Future<Set<String>> fetchFavoriteLotIds() async {
    final userId = await _getUserRowId();
    if (userId == null) return <String>{};
    final rows = await _sb.from('favorites').select('parking_lot_id').eq('user_id', userId);
    return rows.map<String>((e) => (e['parking_lot_id'] as String)).toSet();
  }

  Future<bool> isFavorite(String lotId) async {
    final ids = await fetchFavoriteLotIds();
    return ids.contains(lotId);
  }

  Future<void> toggleFavorite(String lotId) async {
    final userId = await _getUserRowId();
    if (userId == null) throw Exception('로그인이 필요합니다');
    final existing = await _sb
        .from('favorites')
        .select('parking_lot_id')
        .eq('user_id', userId)
        .eq('parking_lot_id', lotId)
        .limit(1);
    if (existing.isNotEmpty) {
      await _sb.from('favorites').delete().eq('user_id', userId).eq('parking_lot_id', lotId);
    } else {
      await _sb.from('favorites').insert({'user_id': userId, 'parking_lot_id': lotId});
    }
  }

  Future<List<Map<String, dynamic>>> fetchFavoriteLots() async {
    final userId = await _getUserRowId();
    if (userId == null) return [];
    final favs = await _sb.from('favorites').select('parking_lot_id').eq('user_id', userId);
    if (favs.isEmpty) return [];
    final ids = favs.map<String>((e) => e['parking_lot_id'] as String).toList();
    // Use in_ to fetch parking lots
    final lots = await _sb.from('parking_lots').select('*').inFilter('id', ids);
    return lots.cast<Map<String, dynamic>>();
  }
}
