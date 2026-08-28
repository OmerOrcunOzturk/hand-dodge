# Hand Dodge

Hand Dodge, Python ile gelistirilmis kamera kontrollu kucuk bir dodge oyunudur.
Oyuncu, kamerada elini saga ve sola hareket ettirerek ekrandaki karakteri
kontrol eder ve yukaridan dusen engellerden kacmaya calisir.

## Portfoy Ozeti

Hand Dodge, bilgisayar gormesi ile oyun mekaniklerini birlestiren interaktif
bir Python projesidir. Pygame oyun dongusunu ve arayuzu yonetirken, OpenCV
kamera goruntusunu isler ve MediaPipe tek el takibiyle oyuncu kontrolunu
saglar. Proje; gercek zamanli kamera kullanimi, temiz sinif yapisi, kaynak
yonetimi, FPS'den bagimsiz hareket ve kullanici odakli kalibrasyon akisi gibi
portfoyde one cikarilabilecek teknik detaylar icerir.

## Proje Aciklamasi

Bu proje; Python, Pygame, OpenCV ve MediaPipe kullanarak temel bilgisayar
gormesi ile oyun gelistirmeyi bir araya getiren portfoy odakli bir prototiptir.
Oyunun amaci, el takibi verisini basit ve oynanabilir bir mekanige donusturmek
ve temiz, okunabilir bir Python kod yapisi ortaya koymaktir.

## Ozellikler

- Kamera ile tek el algilama
- Elin yatay konumuna gore oyuncu kontrolu
- Klavye ile yedek sag-sol kontrol
- Pygame icinde kamera onizlemesi
- Baslangic kalibrasyon ekrani
- Yukaridan dusen rastgele engeller
- Can, skor ve kademeli zorluk sistemi
- Game Over ve Space ile yeniden baslatma

## Kullanilan Teknolojiler

- Python 3.12
- Pygame
- OpenCV
- MediaPipe

## Kurulum

Python 3.12 kullanilmasi onerilir. MediaPipe ve Pygame kurulumunda daha yeni
Python surumleri paket uyumlulugu sorunu cikarabilir.

Windows PowerShell:

```powershell
cd hand_dodge
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS / Linux:

```bash
cd hand_dodge
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Calistirma

```bash
python src/main.py
```

## Kontroller

- Elini kamerada saga ve sola hareket ettirerek oyuncuyu kontrol et.
- El algilanmadiginda sol ve sag ok tuslari yedek kontrol olarak calisir.
- Game Over ekraninda Space tusu ile oyunu yeniden baslat.
- ESC tusu ile oyundan cik.
- Kalibrasyon basarisiz olursa R tusu ile tekrar dene.

## Proje Yapisi

```text
hand_dodge/
|-- assets/
|   |-- fonts/
|   |-- images/
|   `-- sounds/
|-- src/
|   |-- __init__.py
|   |-- camera.py
|   |-- enemy.py
|   |-- game.py
|   |-- hand_tracker.py
|   |-- main.py
|   |-- player.py
|   `-- settings.py
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Teknik Kararlar

- `Game` sinifi oyun dongusunu, event yonetimini, update ve draw adimlarini
  ayri metotlarda toplar.
- `Camera`, kamera kaynagini acma, frame okuma ve guvenli kapatma
  sorumlulugunu tasir.
- `HandTracker`, MediaPipe ile tek el algilar ve wrist landmark uzerinden
  normalize X konumu uretir.
- Oyuncu hareketinde basit linear interpolation kullanilarak el takibinden
  gelen titreme azaltilir.
- Hareket hesaplari FPS'den bagimsiz olmasi icin `delta_time` ile yapilir.
- Kamera goruntusu ayri OpenCV penceresi yerine Pygame icinde kucuk onizleme
  olarak gosterilir.
- Ayni klasordeki moduller `src.` on eki olmadan import edilir.

## Bilinen Sinirlamalar

- Oyun yalnizca tek el algilama uzerine kuruludur.
- Kamera isigi dusukse veya el kadraj disindaysa kontrol kararsiz olabilir.
- High score kaydi bulunmaz.
- Ses, gorsel asset ve menu sistemi henuz yoktur.
- MediaPipe icin Python 3.12 kullanimi onerilir.

## Gelecek Gelistirmeler

- High score kaydi
- Basit ana menu
- Ses efektleri
- Daha iyi oyuncu ve engel gorselleri
- Farkli zorluk modlari
- Paketleme ve kolay calistirilabilir demo surumu

## Ekran Goruntuleri

README icin ekran goruntuleri bu bolume eklenebilir:

```markdown
![Calibration screen](assets/images/calibration.png)
![Gameplay](assets/images/gameplay.png)
![Game over](assets/images/game-over.png)
```

## Demo Videosu

Kisa bir demo videosu icin su akis yeterlidir:

1. Oyunu baslat ve kalibrasyon ekranini goster.
2. Elini kameraya gostererek oyunun basladigini kaydet.
3. Oyuncuyu el hareketiyle saga ve sola kontrol et.
4. Birkac engelden kac ve skorun arttigini goster.
5. Bilerek engele carparak Game Over ekranini goster.
6. Space ile oyunun yeniden basladigini goster.

## GitHub Aciklamasi

Camera-controlled Python dodge game built with Pygame, OpenCV and MediaPipe.

## CV / LinkedIn Aciklamasi

Hand Dodge, Python, Pygame, OpenCV ve MediaPipe kullanarak gelistirdigim kamera
kontrollu bir oyun prototipidir. Projede el takibi verisini oyun kontrolune
donusturdum; skor, can, zorluk artisi, kalibrasyon ve Game Over akisini temiz
bir Python kod yapisiyla uyguladim.

Kamera goruntusunu OpenCV ile alip MediaPipe uzerinden tek el landmark takibi
yaptim; elde edilen normalize X konumunu Pygame tarafinda akici oyuncu
hareketine cevirdim. Proje, gercek zamanli input isleme ve oyun dongusu
tasarimini gosteren paylasilabilir bir portfoy calismasidir.

## Onerilen GitHub Etiketleri

`python`, `pygame`, `opencv`, `mediapipe`, `computer-vision`, `hand-tracking`,
`game-development`, `portfolio-project`
