# Data policy

No speech audio, prompt audio, speaker metadata, ASR transcript, private manifest, checkpoint, or generated waveform is redistributed here.

For FLEURS-based reproductions, download the relevant language and official development/test split directly from the original provider, comply with its license and terms, and build a local manifest with the documented schema:

```json
{"target_id": "stable-id", "audio_path": "local/path.wav", "text": "reference", "split": "development"}
```

The actual experiment manifests contain internal provenance and are deliberately not included. The DDD Khmer source is also not redistributed; its metadata or audio may be used only after independently confirming provider permissions.

`data/manifests/` is intentionally empty: it is a location for a user-created, legally obtained local manifest, not a data release.
