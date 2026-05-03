<p align="center">
  <a href="./README.md">
    <img src="https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.5.0/flags/4x3/gb.svg" alt="English" width="40">
  </a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="./README_tr.md">
    <img src="https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.5.0/flags/4x3/tr.svg" alt="Türkçe" width="40">
  </a>
</p>

---

<p align="center">
    <img width="256" height="256" alt="Fountext_Logo" src="https://github.com/user-attachments/assets/70247045-03b1-4133-8ced-a6de23d3e82f" />
</p>

<h1 align="center">
  Linux için Fountext Senaryo Editörü
</h1>

<p align="center">
  <strong>Python, PyQt6 ve özel bir C++ düzen motoru ile yapılan, işletim sistemi düzeyinde hızlı ve profesyonel bir senaryo yazma ortamı.</strong>
</p>

<p align="center">
  <a href="https://github.com/SametCirik/Fountext-Screenwriting-Editor/releases">
    <img alt="Son Sürüm" src="https://img.shields.io/badge/son%20sürüm-v1.2-blue">
  </a>
  <a href="https://github.com/SametCirik/Fountext-Screenwriting-Editor/blob/master/LICENSE">
    <img alt="Lisans" src="https://img.shields.io/badge/lisans-GPLv3-green">
  </a>
  <a href="https://github.com/SametCirik/Fountext-Screenwriting-Editor">
    <img alt="Platform" src="https://img.shields.io/badge/platform-Linux-important">
  </a>
</p>

---

## Fountext Hakkında

Fountext, **Fountain** söz dizimini tam olarak destekleyen, modern, hafif ve güçlü bir metin senaryosu editörüdür. Biçimlendirme sorunlarından kurtulun; sadece yazın. Fountext'in özel olarak tasarlanmış C++ oluşturma motoru, milimetre-mükemmel konumlandırma sağlar, böylece her şey tam istediğiniz gibi görünür.

### Ana Özellikler

**Fountain Format Desteği** - .fountain senaryo formatı için tam destek  
**Gerçek Zamanlı Oluşturma** - Özel C++ düzen motoru milimetre-mükemmel konumlandırma sağlar  
**Otomatik Biçimlendirme** - Sahne başlıklarını, karakter adlarını ve diyaloğu otomatik olarak biçimlendiriyor  
**Sahne Navigasyonu** - Hızlı sahne/konum navigasyonu için açılır panel  
**PDF Dışarı Aktarma** - Endüstri standardı, metin seçilebilir vektör PDF'lerine dışarı aktarın  
**Yumuşak Kaydırma** - Sahnetler arasında sorunsuz bir şekilde gezinin  
**Sayfa İstatistikleri** - Gerçek zamanlı sayfa sayısı ve karakter sayısı izleme  
**İkili Dil Desteği** - İngilizce ve Türkçe için tam destek  

---

## Hızlı Başlangıç

### Seçenek 1: Hazır Derlenmiş Sürümü İndirin (Çoğu Kullanıcı İçin Önerilen)

1. **[Sürümler (Releases) Sayfasına](https://github.com/SametCirik/Fountext-Screenwriting-Editor/releases) Gidin**

2. **En Güncel Sürümü İndirin**
   - En son sürüme (şu an **v1.2**) tıklayın.
   - `Fountext-v1.2-Linux.tar.gz` dosyasını indirin.

3. **Arşivi Çıkartın**

   \```bash
   # Arşivi klasöre çıkartın
   tar -xzf Fountext-v1.2-Linux.tar.gz
   
   # Klasörün içine girin
   cd Fountext
   \```

4. **Nasıl Çalıştıracağınızı Seçin:**

   - **A. Taşınabilir (Portable) Mod**
     Hiçbir kurulum yapmadan Fountext'i anında çalıştırabilirsiniz. Klasördeki `Fountext` çalıştırılabilir dosyasına çift tıklayın veya terminal üzerinden çalıştırın:
     \```bash
     ./Fountext
     \```
     *(Not: Taşınabilir modda çalıştırıldığında, işletim sisteminize veya Wayland ayarlarınıza bağlı olarak görev çubuğunda uygulama logosu görünmeyebilir).*

   - **B. Sisteme Kurulum Modu (KDE/Wayland İçin Önerilir)**
     Fountext logosunun görev çubuğunda kusursuz görünmesini ve uygulamayı sisteminizin Başlat/Uygulamalar menüsünde (Ofis sekmesi altında) bulmak istiyorsanız kurulum betiğini çalıştırın:
     \```bash
     ./install.sh
     \```
     Bu işlem Fountext'i sisteminize güvenle entegre edecektir. Ayrıca kolay erişim için klasörün içinde şık logolu bir `Fountext.desktop` kısayolu oluşturulacaktır!

### Seçenek 2: Kaynak Koddan Derleme

#### Gereksinimler

- **Python 3.8+**
- **PyQt6**
- **CMake 3.15+**
- **C++ derleyici** (GCC 7+ veya Clang)
- **pybind11**

#### Kurulum Adımları

1. **Depoyu Klonlayın**

   \```bash
   git clone https://github.com/SametCirik/Fountext-Screenwriting-Editor.git
   cd Fountext-Screenwriting-Editor
   \```

2. **Python Bağımlılıklarını Kurun**

   \```bash
   pip install -r requirements.txt
   \```

3. **C++ Düzen Motorunu (Layout Engine) Derleyin**

   \```bash
   mkdir build
   cd build
   cmake ..
   make
   cd ..
   \```

4. **Uygulamayı Çalıştırın**

   \```bash
   python src/main.py
   \```

---

## Katkıda Bulunma ve Çatallama

Katkılarınızı bekliyoruz! İşte başlamak için nasıl yapacağınız:

### Depoyu Çatallandırın

1. **[Ana depo sayfasının](https://github.com/SametCirik/Fountext-Screenwriting-Editor) sağ üstündeki "Fork" düğmesine tıklayın**
   - Bu, deponun bir kopyasını GitHub hesabınızın altında oluşturur

2. **Çatallanan Deponuzu Klonlayın**
   ```bash
   git clone https://github.com/KULLANICI_ADINIZ/Fountext-Screenwriting-Editor.git
   cd Fountext-Screenwriting-Editor
   ```

3. **Değişiklikleriniz için Bir Dal Oluşturun**
   ```bash
   git checkout -b feature/ozellik-adiniz
   # veya
   git checkout -b fix/hata-duzelti-adiniz
   ```

4. **Değişiklik Yapın ve Kaydedin**
   ```bash
   git add .
   git commit -m "Değişikliklerinizin açık bir açıklaması"
   ```

5. **Çatallandırılmış Deponuza Gönderin**
   ```bash
   git push origin feature/ozellik-adiniz
   ```

6. **Bir Çekme İsteği Oluşturun**
   - [Ana depoya](https://github.com/SametCirik/Fountext-Screenwriting-Editor) gidin
   - "Pull Requests" → "New Pull Request" öğesine tıklayın
   - Çatallanan deponuzu ve dalınızı seçin
   - Değişikliklerinizi açıklayın ve gönderin!

### Katkı Yapılabilecek Alanlar

- **Hata Düzeltmeleri** - Bir sorun mu buldunuz? Düzeltmeye yardım edin!
- **Özellikler** - Bir fikriniz mi var? Uygulayın!
- **Belgeler** - Kılavuzları ve belgeleri iyileştirmeye yardım edin
- **Çeviriler** - Yeni diller için destek ekleyin
- **Test Etme** - Sorunları bildirin ve yeni özellikleri test edin

---

## Kullanım Kılavuzu

### Temel Yazma

1. **Yazmaya Başlayın** - Uygulamayı açın ve Fountain formatında yazmaya başlayın
2. **Otomatik Biçimlendirme** - Sahne başlıkları, karakter adları ve diyalog otomatik olarak biçimlendirilir
3. **Sahnelerde Gezinin** - Konumlar arasında atlamak için "SAHNELER" menüsüne tıklayın

### Dışarı Aktarma

- **PDF Dışarı Aktarma** - `Dosya → PDF Olarak Dışarı Aktar` veya `Ctrl + E` tuşlarına basın
- Profesyonel endüstri standardı biçimlendirmesi
- Metin seçilebilir içerik
- Vektör tabanlı oluşturma

### Proje Yapısı

```
Fountext-Screenwriting-Editor/
├── src/                    # Python kaynak kodu
├── src_cpp/                # C++ düzen motoru kaynağı
├── requirements.txt        # Python bağımlılıkları
├── CMakeLists.txt         # C++ derleme yapılandırması
├── guide_EN.pdf           # Kullanıcı Kılavuzu (İngilizce)
├── guide_TR.pdf           # Kullanıcı Kılavuzu (Türkçe)
└── README.md              # Bu dosya
```

---

## Sistem Gereksinimleri

- **İşletim Sistemi**: Linux (Ubuntu 20.04+, Fedora 33+, Debian 11+ veya benzer)
- **Python**: 3.8 veya daha yüksek
- **RAM**: Minimum 512 MB, 2 GB tavsiye edilir
- **Disk Alanı**: Kurulum için ~200 MB

---

## Belgeler

- **[Kullanıcı Kılavuzu (İngilizce)](./guide_EN.pdf)** - Fountain formatında tam kullanıcı kılavuzu
- **[Kullanıcı Kılavuzu (Türkçe)](./guide_TR.pdf)** - Türkçe kullanıcı rehberi

---

## Lisans

Bu proje **GNU Genel Kamu Lisansı v3.0** altında lisanslanmıştır - Ayrıntılar için [LİSANS](./LICENSE) dosyasına bakın.

---

## Destek ve Topluluk

- **Sorunlar** - Bir hata mı buldunuz? [Buradan bildirin](https://github.com/SametCirik/Fountext-Screenwriting-Editor/issues)
- **Tartışmalar** - Sorularınız mı var? [Bir tartışma başlatın](https://github.com/SametCirik/Fountext-Screenwriting-Editor/discussions)
- **İletişim** - [GitHub](https://github.com/SametCirik) üzerinden ulaşın

---

## Yol Haritası

- [ ] Çapraz platform desteği (Windows, macOS)
- [ ] Ek dışarı aktarma formatları (FDXM, AV Pro)
- [ ] İşbirliği özellikleri
- [ ] Tema özelleştirmesi
- [ ] Eklenti sistemi

---

## Teşekkürler

Şunlarla oluşturulmuştur:
- **Python** - Temel uygulama mantığı
- **PyQt6** - Kullanıcı arayüzü
- **C++17** - Yüksek performanslı düzen motoru
- **pybind11** - Python/C++ bağlamaları
- **Fountain Format** - Endüstri standardı senaryo söz dizimi

---

## Soruların mı Var?

Herhangi bir soru için bir [sorun](https://github.com/SametCirik/Fountext-Screenwriting-Editor/issues) veya [tartışma](https://github.com/SametCirik/Fountext-Screenwriting-Editor/discussions) açmaktan çekinmeyin.

**Mutlu yazılar!**