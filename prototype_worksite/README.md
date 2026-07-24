# Worksite prototype — the deployed edge module (pose + fall + posture-strain index + PPE + fire)

This is the full in-browser worksite module of SHine-K, provided so the
"Working" implementation-status claims in the paper (Table II) are directly
runnable and verifiable. The paper's fall-detection evaluation is a faithful
port of the `analyzePerson()` logic in `worksite_multi.html`.

Unlike the pared-down public live demo (which surfaces pose + fall), this module
also runs **in-browser PPE detection** with a real YOLOv11 model via
ONNX Runtime Web (WebAssembly), entirely on-device.

## Contents
- `worksite_multi.html` — multi-person worksite edge node (MoveNet MultiPose via TF.js, on-device)
- `ppe.js` — PPE detector plugin (YOLOv11 ONNX, `onnxruntime-web`; helmet / mask / vest)
- `ppe.onnx` — the trained PPE model (YOLOv11, exported to ONNX; ~10.6 MB)
- `transport.js` — swappable event transport (BroadcastChannel / WebSocket / public MQTT broker)
- `store.js` — local event log / JSON export
- `PPE_HOWTO.md` — how the PPE model is exported (`best.pt` → `ppe.onnx`) and class-order notes

## Run it (any static server + a webcam)
```bash
python3 -m http.server 8080
# then open http://localhost:8080/worksite_multi.html and allow the camera
```
- Multi-person MoveNet pose, the fall/inactivity state machine, and the two-cue
  posture-strain index (a REBA-inspired proxy, not a REBA score) run per person on-device.
- With `ppe.onnx` present (included here), each camera is checked for
  helmet / vest / mask; a missing item raises a PPE event.
- Only de-identified skeleton coordinates and structured events are sent over
  the transport — no pixels leave the page during routine operation.

## Notes
- The public-broker option uses the free `broker.emqx.io` endpoint for
  demonstration only; a deployment would use TLS transport with per-site topic
  authentication (see the paper, Section on consent governance).
- The PPE model is trained on a public construction-PPE dataset; the class order
  in `ppe.js` (`NAMES`) must match the training `dataset.yaml`.
