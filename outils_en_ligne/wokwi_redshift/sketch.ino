// WOKWI-REDSHIFT : anneau 12 gradué (jumeau TEST-89).
// Coller dans wokwi.com (Arduino Uno), moniteur série : 12 fréquences.
// Comparer à exp89.json.
#define N 12
float th[N], om[N];
int adj[N][N];
// LCG embarqué (identique au jumeau TEST-89)
static unsigned long _s = 1;
float arand() {
  _s = 1103515245UL * _s + 12345UL;
  return (_s & 0x7fffffff) / 2147483647.0;
}

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++) adj[i][j] = 0;
  for (int i = 0; i < N; i++) {
    adj[i][(i - 1 + N) % N] = 1; adj[i][(i + 1) % N] = 1;
    om[i] = -1.0 * exp(-i / 3.0);
  }
  _s = 84;
  for (int i = 0; i < N; i++) th[i] = arand() * 2 * PI;
  float first[N], last[N];
  for (int t = 0; t < 3000; t++) {
    if (t == 2500) for (int i = 0; i < N; i++) first[i] = th[i];
    float nth[N];
    for (int i = 0; i < N; i++) {
      float s = 0;
      for (int j = 0; j < N; j++) if (adj[i][j]) s += sin(th[j] - th[i]);
      nth[i] = th[i] + 0.1 * (om[i] + (3.0 / N) * s);
    }
    for (int i = 0; i < N; i++) th[i] = nth[i];
  }
  for (int i = 0; i < N; i++) last[i] = th[i];
  for (int i = 0; i < N; i++) {
    float f = (last[i] - first[i]) / (500 * 0.1);
    Serial.print("osc"); Serial.print(i);
    Serial.print(" freq="); Serial.println(f, 4);
  }
}
void loop() {}
