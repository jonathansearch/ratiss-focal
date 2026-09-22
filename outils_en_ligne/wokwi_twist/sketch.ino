// WOKWI-TWIST : anneau 24 + hubs, 2 puits (jumeau TEST-88).
// Coller dans wokwi.com (nouveau projet Arduino Uno), ouvrir le moniteur
// série : affiche R et twist pour G0=0 puis G0=1. Comparer à exp88.json.
#define NQ 24
float th[NQ], om[NQ], prof[NQ];
int adj[NQ][NQ];
// LCG embarqué (identique au jumeau TEST-88, pas le random() Arduino)
static unsigned long _s = 1;
float arand() {
  _s = 1103515245UL * _s + 12345UL;
  return (_s & 0x7fffffff) / 2147483647.0;
}

void build() {
  for (int i = 0; i < NQ; i++)
    for (int j = 0; j < NQ; j++) adj[i][j] = 0;
  for (int i = 0; i < NQ; i++) {
    adj[i][(i - 1 + NQ) % NQ] = 1; adj[i][(i + 1) % NQ] = 1;
  }
  for (int j = 0; j < NQ; j++) { adj[0][j] = 1; adj[j][0] = 1; adj[12][j] = 1; adj[j][12] = 1; }
  for (int i = 0; i < NQ; i++) adj[i][i] = 0;
  for (int i = 0; i < NQ; i++) {
    float a = 2 * PI * i / NQ;
    float d0 = fabs(fmod(a + PI, 2 * PI) - PI);
    float d1 = fabs(fmod(a - PI + PI, 2 * PI) - PI);
    prof[i] = exp(-d0 * d0 / 0.5) + exp(-d1 * d1 / 0.5);
  }
}

void run(float G0) {
  _s = 100;
  for (int i = 0; i < NQ; i++) th[i] = arand() * 2 * PI;
  _s = 55;
  for (int i = 0; i < NQ; i++) {
    float u1 = max(arand(), 1e-6), u2 = arand();
    om[i] = 0.2 * sqrt(-2 * log(u1)) * cos(2 * PI * u2) - G0 * prof[i];
  }
  float Rlast[50]; int ri = 0;
  for (int t = 0; t < 300; t++) {
    float nth[NQ];
    for (int i = 0; i < NQ; i++) {
      float s = 0;
      for (int j = 0; j < NQ; j++) if (adj[i][j]) s += sin(th[j] - th[i]);
      nth[i] = th[i] + 0.3 * (om[i] + (3.0 / NQ) * s);
    }
    for (int i = 0; i < NQ; i++) th[i] = nth[i];
    float sr = 0, si = 0;
    for (int i = 0; i < NQ; i++) { sr += cos(th[i]); si += sin(th[i]); }
    Rlast[ri % 50] = sqrt(sr * sr + si * si) / NQ; ri++;
  }
  float Rm = 0; for (int i = 0; i < 50; i++) Rm += Rlast[i]; Rm /= 50;
  float tw = 0;
  for (int i = 0; i < NQ; i++) {
    float d = th[(i + 1) % NQ] - th[i];
    tw += atan2(sin(d), cos(d));
  }
  tw /= 2 * PI;
  Serial.print("G0="); Serial.print(G0);
  Serial.print(" R="); Serial.print(Rm, 4);
  Serial.print(" twist="); Serial.println(tw, 3);
}

void setup() {
  Serial.begin(115200); delay(1000); build();
  Serial.println("--- debut ---"); Serial.flush();
  run(0.0); Serial.flush(); delay(300);
  run(1.0); Serial.flush(); delay(300);
  Serial.println("--- fin ---"); Serial.flush();
}
void loop() {}
