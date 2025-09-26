import 'dart:io';

import 'package:supabase_flutter/supabase_flutter.dart';

class StorageService {
  StorageService(this._sb);
  final SupabaseClient _sb;
  static const String bucket = 'parking-images';

  Future<List<String>> listLotImages(String lotId) async {
    final path = 'lots/$lotId/';
    final res = await _sb.storage.from(bucket).list(path: path);
    return res.map((f) => _sb.storage.from(bucket).getPublicUrl('$path${f.name}')).toList();
  }

  Future<void> uploadLotImage(String lotId, File file) async {
    final path = 'lots/$lotId/${DateTime.now().millisecondsSinceEpoch}_${file.path.split('/').last}';
    await _sb.storage.from(bucket).upload(path, file);
    await _sb.storage.from(bucket).createSignedUrl(path, 60); // warm up
  }
}
