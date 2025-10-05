/**
 * @typedef {{ x: number, y: number, z: number }} Vector3
 *
 * @typedef {{ r_au: Vector3, v_au_per_day: Vector3 }} Heliocentric
 *
 * @typedef {{ r_au: Vector3, v_au_per_day: Vector3 }} Geocentric
 *
 * @typedef {{ iso: string, heliocentric: Heliocentric, geocentric: Geocentric }} Timeline
 *
 * @typedef {{
 *   frame: string,
 *   units: { position: string, velocity: string },
 *   epoch_iso: string,
 *   impact_iso: string,
 *   time_step_days: number,
 *   earth_at_epoch: Heliocentric,
 *   asteroid_epoch_state: { id: string, r_au: Vector3, v_au_per_day: Vector3 }
 * }} Metadata
 *
 * @typedef {{ metadata: Metadata, timeline: Timeline[] }} OrbitData
 */
