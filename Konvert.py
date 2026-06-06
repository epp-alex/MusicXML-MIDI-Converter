import os
import sys
import json
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog

# music21 Versuch zu importieren
try:
    from music21 import converter
    MUSIC21_AVAILABLE = True
except Exception:
    MUSIC21_AVAILABLE = False

SUPPORTED_EXT = ('.xml', '.musicxml', '.mxl')
APP_NAME      = "MusicXML_MIDI_Konverter"


# ──────────────────────────────────────────────
#  Übersetzungen / Translations / Переводы / Переклади
# ──────────────────────────────────────────────

TRANSLATIONS = {
"de": {
        "window_title":        "MusicXML → MIDI Konverter",
        "btn_browse":          "Ordner wählen",
        "btn_start":           "START / AKTUALISIEREN",
        "btn_start_running":   "Läuft …",
        "btn_stop":            "STOP",
        "label_ready":         "Bereit für neue Lieder",
        "label_ready2":        "Bereit für weitere Lieder",
        "config_info":         "Einstellungen gespeichert in: {}",
        "log_no_music21":      "⚠  WARNUNG: music21 ist nicht installiert!\n   Bitte ausführen:  pip install music21",
        "log_music21_ok":      "✓  music21 gefunden – bereit zur Konvertierung.",
        "log_last_path":       "   Letzter Pfad geladen: {}",
        "log_folder_chosen":   "   Ordner gewählt: {}",
        "log_new_scan":        "\n--- Neuer Suchlauf gestartet ---",
        "log_abort_req":       "   ⏹  Abbruch angefordert …",
        "err_no_music21":      "FEHLER: music21 nicht installiert!",
        "err_no_dir":          "FEHLER: Ordner existiert nicht: {}",
        "log_no_files":        "Keine XML/MXL-Dateien im Ordner gefunden.",
        "progress_files":      "{} / {} Dateien …",
        "log_aborted":         "   ⏹  Abgebrochen.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Plan B): {} gerettet.",
        "log_info_c":          "   INFO: {} – nutze Plan C (nur Noten) …",
        "log_ok_c":            "✓  OK (Plan C): {} (nur Noten-Stream)",
        "log_error_file":      "✗  FEHLER bei {}: {}",
        "log_done":            "\n--- FERTIG ---\n   Erstellt: {}  |  Fehler: {}",
        "language_label":      "Sprache:"
    },
    "en": {
        "window_title":        "MusicXML → MIDI Converter",
        "btn_browse":          "Select Folder",
        "btn_start":           "START / REFRESH",
        "btn_start_running":   "Running …",
        "btn_stop":            "STOP",
        "label_ready":         "Ready for new songs",
        "label_ready2":        "Ready for more songs",
        "config_info":         "Settings saved in: {}",
        "log_no_music21":      "⚠  WARNING: music21 is not installed!\n   Please run:  pip install music21",
        "log_music21_ok":      "✓  music21 found – ready for conversion.",
        "log_last_path":       "   Last path loaded: {}",
        "log_folder_chosen":   "   Folder selected: {}",
        "log_new_scan":        "\n--- New scan started ---",
        "log_abort_req":       "   ⏹  Cancellation requested …",
        "err_no_music21":      "ERROR: music21 is not installed!",
        "err_no_dir":          "ERROR: Folder does not exist: {}",
        "log_no_files":        "No XML/MXL files found in the folder.",
        "progress_files":      "{} / {} files …",
        "log_aborted":         "   ⏹  Aborted.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Plan B): {} recovered.",
        "log_info_c":          "   INFO: {} – using Plan C (notes only) …",
        "log_ok_c":            "✓  OK (Plan C): {} (notes stream only)",
        "log_error_file":      "✗  ERROR in {}: {}",
        "log_done":            "\n--- DONE ---\n   Created: {}  |  Errors: {}",
        "language_label":      "Language:"
    },
    "fr": {
        "window_title":        "Convertisseur MusicXML → MIDI",
        "btn_browse":          "Choisir un dossier",
        "btn_start":           "DÉMARRER / ACTUALISER",
        "btn_start_running":   "En cours …",
        "btn_stop":            "ARRÊTER",
        "label_ready":         "Prêt pour de nouvelles chansons",
        "label_ready2":        "Prêt pour d'autres chansons",
        "config_info":         "Paramètres enregistrés dans : {}",
        "log_no_music21":      "⚠  ATTENTION : music21 n'est pas installé !\n   Veuillez exécuter :  pip install music21",
        "log_music21_ok":      "✓  music21 trouvé – prêt pour la conversion.",
        "log_last_path":       "   Dernier chemin chargé : {}",
        "log_folder_chosen":   "   Dossier choisi : {}",
        "log_new_scan":        "\n--- Nouvelle recherche démarrée ---",
        "log_abort_req":       "   ⏹  Annulation demandée …",
        "err_no_music21":      "ERREUR : music21 n'est pas installé !",
        "err_no_dir":          "ERREUR : Le dossier n'existe pas : {}",
        "log_no_files":        "Aucun fichier XML/MXL trouvé dans le dossier.",
        "progress_files":      "{} / {} fichiers …",
        "log_aborted":         "   ⏹  Annulé.",
        "log_ok":              "✓  OK : {}",
        "log_ok_b":            "✓  OK (Plan B) : {} récupéré.",
        "log_info_c":          "   INFO : {} – utilisation du Plan C (notes uniquement) …",
        "log_ok_c":            "✓  OK (Plan C) : {} (flux de notes uniquement)",
        "log_error_file":      "✗  ERREUR dans {} : {}",
        "log_done":            "\n--- TERMINÉ ---\n   Créés : {}  |  Erreurs : {}",
        "language_label":      "Langue :"
    },
    "es": {
        "window_title":        "Convertidor MusicXML → MIDI",
        "btn_browse":          "Seleccionar carpeta",
        "btn_start":           "INICIAR / ACTUALIZAR",
        "btn_start_running":   "Ejecutando …",
        "btn_stop":            "DETENER",
        "label_ready":         "Listo para nuevas canciones",
        "label_ready2":        "Listo para más canciones",
        "config_info":         "Ajustes guardados en: {}",
        "log_no_music21":      "⚠  ADVERTENCIA: ¡music21 no está instalado!\n   Por favor ejecute:  pip install music21",
        "log_music21_ok":      "✓  music21 encontrado – listo para la conversión.",
        "log_last_path":       "   Última ruta cargada: {}",
        "log_folder_chosen":   "   Carpeta seleccionada: {}",
        "log_new_scan":        "\n--- Nuevo escaneo iniciado ---",
        "log_abort_req":       "   ⏹  Cancelación solicitada …",
        "err_no_music21":      "ERROR: ¡music21 no está instalado!",
        "err_no_dir":          "ERROR: La carpeta no existe: {}",
        "log_no_files":        "No se encontraron archivos XML/MXL en la carpeta.",
        "progress_files":      "{} / {} archivos …",
        "log_aborted":         "   ⏹  Cancelado.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Plan B): {} recuperado.",
        "log_info_c":          "   INFO: {} – usando Plan C (solo notas) …",
        "log_ok_c":            "✓  OK (Plan C): {} (solo flujo de notas)",
        "log_error_file":      "✗  ERROR en {}: {}",
        "log_done":            "\n--- FINALIZADO ---\n   Creados: {}  |  Errores: {}",
        "language_label":      "Idioma:"
    },
    "it": {
        "window_title":        "Convertitore MusicXML → MIDI",
        "btn_browse":          "Seleziona cartella",
        "btn_start":           "AVVIA / AGGIORNA",
        "btn_start_running":   "In corso …",
        "btn_stop":            "FERMA",
        "label_ready":         "Pronto per nuovi brani",
        "label_ready2":        "Pronto per altri brani",
        "config_info":         "Impostazioni salvate in: {}",
        "log_no_music21":      "⚠  AVVISO: music21 non è installato!\n   Esegui:  pip install music21",
        "log_music21_ok":      "✓  music21 trovato – pronto per la conversione.",
        "log_last_path":       "   Ultimo percorso caricato: {}",
        "log_folder_chosen":   "   Cartella selezionata: {}",
        "log_new_scan":        "\n--- Nuova scansione avviata ---",
        "log_abort_req":       "   ⏹  Annullamento richiesto …",
        "err_no_music21":      "ERRORE: music21 non è installato!",
        "err_no_dir":          "ERRORE: La cartella non esiste: {}",
        "log_no_files":        "Nessun file XML/MXL trovato nella cartella.",
        "progress_files":      "{} / {} file …",
        "log_aborted":         "   ⏹  Annullato.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Plan B): {} recuperato.",
        "log_info_c":          "   INFO: {} – utilizzo Piano C (solo note) …",
        "log_ok_c":            "✓  OK (Piano C): {} (solo flusso di note)",
        "log_error_file":      "✗  ERRORE in {}: {}",
        "log_done":            "\n--- COMPLETATO ---\n   Creati: {}  |  Errori: {}",
        "language_label":      "Lingua:"
    },
    "nl": {
        "window_title":        "MusicXML → MIDI Convertor",
        "btn_browse":          "Map selecteren",
        "btn_start":           "START / VERNIEUWEN",
        "btn_start_running":   "Bezig …",
        "btn_stop":            "STOP",
        "label_ready":         "Gereed voor nieuwe nummers",
        "label_ready2":        "Gereed voor meer nummers",
        "config_info":         "Instellingen opgeslagen in: {}",
        "log_no_music21":      "⚠  WAARSCHUWING: music21 is nicht geïnstalleerd!\n   Voer uit:  pip install music21",
        "log_music21_ok":      "✓  music21 gevonden – klaar voor conversie.",
        "log_last_path":       "   Laatste pad geladen: {}",
        "log_folder_chosen":   "   Map gekozen: {}",
        "log_new_scan":        "\n--- Nieuwe scan gestart ---",
        "log_abort_req":       "   ⏹  Afbreken aangevraagd …",
        "err_no_music21":      "FOUT: music21 niet geïnstalleerd!",
        "err_no_dir":          "FOUT: Map bestaat niet: {}",
        "log_no_files":        "Geen XML/MXL-bestanden in de map gevonden.",
        "progress_files":      "{} / {} bestanden …",
        "log_aborted":         "   ⏹  Afgebroken.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Plan B): {} gered.",
        "log_info_c":          "   INFO: {} – gebruik Plan C (alleen noten) …",
        "log_ok_c":            "✓  OK (Plan C): {} (alleen noten-stream)",
        "log_error_file":      "✗  FOUT bij {}: {}",
        "log_done":            "\n--- KLAAR ---\n   Gemaakt: {}  |  Fouten: {}",
        "language_label":      "Taal:"
    },
    "pl": {
        "window_title":        "Konwerter MusicXML → MIDI",
        "btn_browse":          "Wybierz folder",
        "btn_start":           "START / ODŚWIEŻ",
        "btn_start_running":   "Uruchomiono …",
        "btn_stop":            "STOP",
        "label_ready":         "Gotowy na nowe utwory",
        "label_ready2":        "Gotowy na więcej utworów",
        "config_info":         "Ustawienia zapisane w: {}",
        "log_no_music21":      "⚠  OSTRZEŻENIE: music21 nie jest zainstalowane!\n   Uruchom:  pip install music21",
        "log_music21_ok":      "✓  music21 znalezione – gotowe do konwersji.",
        "log_last_path":       "   Ostatnia ścieżka załadowana: {}",
        "log_folder_chosen":   "   Wybrany folder: {}",
        "log_new_scan":        "\n--- Rozpoczęto nowe skanowanie ---",
        "log_abort_req":       "   ⏹  Zażądano przerwania …",
        "err_no_music21":      "BŁĄD: music21 nie jest zainstalowane!",
        "err_no_dir":          "BŁĄD: Folder nie istnieje: {}",
        "log_no_files":        "Nie znaleziono plików XML/MXL w folderze.",
        "progress_files":      "Pliki: {} / {} …",
        "log_aborted":         "   ⏹  Przerwano.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Plan B): Uratowano {}.",
        "log_info_c":          "   INFO: {} – używam Planu C (tylko nuty) …",
        "log_ok_c":            "✓  OK (Plan C): {} (tylko strumień nut)",
        "log_error_file":      "✗  BŁĄD przy {}: {}",
        "log_done":            "\n--- GOTOWE ---\n   Utworzono: {}  |  Błędy: {}",
        "language_label":      "Język:"
    },
    "cs": {
        "window_title":        "Konvertor MusicXML → MIDI",
        "btn_browse":          "Vybrat složku",
        "btn_start":           "START / AKTUALIZOVAT",
        "btn_start_running":   "Běží …",
        "btn_stop":            "STOP",
        "label_ready":         "Připraveno pro nové skladby",
        "label_ready2":        "Připraveno pro další skladby",
        "config_info":         "Nastavení uloženo v: {}",
        "log_no_music21":      "⚠  VAROVÁNÍ: music21 není nainstalováno!\n   Spusťte prosím:  pip install music21",
        "log_music21_ok":      "✓  music21 nalezeno – připraveno ke konverzi.",
        "log_last_path":       "   Načtena poslední cesta: {}",
        "log_folder_chosen":   "   Vybraná složka: {}",
        "log_new_scan":        "\n--- Spuštěno nové hledání ---",
        "log_abort_req":       "   ⏹  Požadováno přerušení …",
        "err_no_music21":      "CHYBA: music21 není nainstalováno!",
        "err_no_dir":          "CHYBA: Složka neexistuje: {}",
        "log_no_files":        "Ve složce nebyly nalezeny žádné soubory XML/MXL.",
        "progress_files":      "{} / {} souborů …",
        "log_aborted":         "   ⏹  Přerušeno.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Plán B): {} zachráněno.",
        "log_info_c":          "   INFO: {} – použijte Plán C (pouze noty) …",
        "log_ok_c":            "✓  OK (Plán C): {} (pouze notový stream)",
        "log_error_file":      "✗  CHYBA u {}: {}",
        "log_done":            "\n--- HOTOVO ---\n   Vytvořeno: {}  |  Chyby: {}",
        "language_label":      "Jazyk:"
    },
    "ru": {
        "window_title":        "Конвертер MusicXML → MIDI",
        "btn_browse":          "Выбрать папку",
        "btn_start":           "СТАРТ / ОБНОВИТЬ",
        "btn_start_running":   "Выполняется …",
        "btn_stop":            "СТОП",
        "label_ready":         "Готов к новым песням",
        "label_ready2":        "Готов к следующим песням",
        "config_info":         "Настройки сохранены в: {}",
        "log_no_music21":      "⚠  ВНИМАНИЕ: music21 не установлен!\n   Пожалуйста, выполните:  pip install music21",
        "log_music21_ok":      "✓  music21 найден – готов к конвертации.",
        "log_last_path":       "   Загружен последний путь: {}",
        "log_folder_chosen":   "   Выбрана папка: {}",
        "log_new_scan":        "\n--- Запущено новое сканирование ---",
        "log_abort_req":       "   ⏹  Запрошена отмена …",
        "err_no_music21":      "ОШИБКА: music21 не установлен!",
        "err_no_dir":          "ОШИБКА: Папка не существует: {}",
        "log_no_files":        "Файлы XML/MXL в папке не найдены.",
        "progress_files":      "{} / {} файлов …",
        "log_aborted":         "   ⏹  Отменено.",
        "log_ok":              "✓  ОК: {}",
        "log_ok_b":            "✓  ОК (План Б): {} спасен.",
        "log_info_c":          "   INFO: {} – использую План С (только ноты) …",
        "log_ok_c":            "✓  ОК (План С): {} (только поток нот)",
        "log_error_file":      "✗  ОШИБКА в {}: {}",
        "log_done":            "\n--- ГОТОВО ---\n   Создано: {}  |  Ошибок: {}",
        "language_label":      "Язык:"
    },
    "uk": {
        "window_title":        "Конвертер MusicXML → MIDI",
        "btn_browse":          "Обрати папку",
        "btn_start":           "СТАРТ / ОНОВИТИ",
        "btn_start_running":   "Виконується …",
        "btn_stop":            "СТОП",
        "label_ready":         "Готовий до нових пісень",
        "label_ready2":        "Готовий до наступних пісень",
        "config_info":         "Налаштування збережено в: {}",
        "log_no_music21":      "⚠  УВАГА: music21 не встановлено!\n   Будь ласка, виконайте:  pip install music21",
        "log_music21_ok":      "✓  music21 знайдено – готовий до конвертації.",
        "log_last_path":       "   Завантажено останній шлях: {}",
        "log_folder_chosen":   "   Обрано папку: {}",
        "log_new_scan":        "\n--- Запущено нове сканування ---",
        "log_abort_req":       "   ⏹  Запитано скасування …",
        "err_no_music21":      "ПОМИЛКА: music21 не встановлено!",
        "err_no_dir":          "ПОМИЛКА: Папка не існує: {}",
        "log_no_files":        "Файлів XML/MXL у папці не знайдено.",
        "progress_files":      "{} / {} файлів …",
        "log_aborted":         "   ⏹  Скасовано.",
        "log_ok":              "✓  ОК: {}",
        "log_ok_b":            "✓  ОК (План Б): {} врятовано.",
        "log_info_c":          "   INFO: {} – використовую План С (тільки ноти) …",
        "log_ok_c":            "✓  ОК (План С): {} (тільки потік нот)",
        "log_error_file":      "✗  ПОМИЛКА у {}: {}",
        "log_done":            "\n--- ГОТОВО ---\n   Створено: {}  |  Помилок: {}",
        "language_label":      "Мова:"
    },
        "tr": {
        "window_title":        "MusicXML → MIDI Dönüştürücü",
        "btn_browse":          "Klasör Seç",
        "btn_start":           "BAŞLAT / YENİLE",
        "btn_start_running":   "Çalışıyor …",
        "btn_stop":            "DURDUR",
        "label_ready":         "Yeni şarkılar için hazır",
        "label_ready2":        "Daha fazla şarkı için hazır",
        "config_info":         "Ayarlar buraya kaydedildi: {}",
        "log_no_music21":      "⚠  UYARI: music21 yüklü değil!\n   Lütfen çalıştırın:  pip install music21",
        "log_music21_ok":      "✓  music21 bulundu – dönüştürme için hazır.",
        "log_last_path":       "   Son yüklenen yol: {}",
        "log_folder_chosen":   "   Seçilen klasör: {}",
        "log_new_scan":        "\n--- Yeni tarama başlatıldı ---",
        "log_abort_req":       "   ⏹  İptal talebi alındı …",
        "err_no_music21":      "HATA: music21 yüklü değil!",
        "err_no_dir":          "HATA: Klasör mevcut değil: {}",
        "log_no_files":        "Klasörde XML/MXL dosyası bulunamadı.",
        "progress_files":      "{} / {} dosya …",
        "log_aborted":         "   ⏹  İptal edildi.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Plan B): {} kurtarıldı.",
        "log_info_c":          "   BİLGİ: {} – Plan C kullanılıyor (sadece notalar) …",
        "log_ok_c":            "✓  OK (Plan C): {} (sadece nota akışı)",
        "log_error_file":      "✗  HATA - {}: {}",
        "log_done":            "\n--- BİTTİ ---\n   Oluşturulan: {}  |  Hata: {}",
        "language_label":      "Dil:"
    },
    "el": {
        "window_title":        "Μετατροπέας MusicXML → MIDI",
        "btn_browse":          "Επιλογή φακέλου",
        "btn_start":           "ΕΚΚΙΝΗΣΗ / ΑΝΑΝΕΩΣΗ",
        "btn_start_running":   "Εκτελείται …",
        "btn_stop":            "ΔΙΑΚΟΠΗ",
        "label_ready":         "Έτοιμο για νέα τραγούδια",
        "label_ready2":        "Έτοιμο για περισσότερα τραγούδια",
        "config_info":         "Οι ρυθμίσεις αποθηκεύτηκαν στο: {}",
        "log_no_music21":      "⚠  ΠΡΟΕΙΔΟΠΟΙΗΣΗ: Το music21 δεν είναι εγκατεστημένο!\n   Παρακαλώ εκτελέστε:  pip install music21",
        "log_music21_ok":      "✓  Το music21 βρέθηκε – έτοιμο για μετατροπή.",
        "log_last_path":       "   Φορτώθηκε η τελευταία διαδρομή: {}",
        "log_folder_chosen":   "   Επιλέχθηκε ο φάκελος: {}",
        "log_new_scan":        "\n--- Ξεκίνησε νέα σάρωση ---",
        "log_abort_req":       "   ⏹  Ζητήθηκε ακύρωση …",
        "err_no_music21":      "ΣΦΑΛΜΑ: Το music21 δεν είναι εγκατεστημένο!",
        "err_no_dir":          "ΣΦΑΛΜΑ: Ο φάκελος δεν υπάρχει: {}",
        "log_no_files":        "Δεν βρέθηκαν αρχεία XML/MXL στον φάκελο.",
        "progress_files":      "{} / {} αρχεία …",
        "log_aborted":         "   ⏹  Ακυρώθηκε.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Σχέδιο Β): Το αρχείο {} διασώθηκε.",
        "log_info_c":          "   ΠΛΗΡΟΦΟΡΙΑ: {} – χρήση Σχεδίου Γ (μόνο νότες) …",
        "log_ok_c":            "✓  OK (Σχέδιο Γ): {} (μόνο ροή νοτών)",
        "log_error_file":      "✗  ΣΦΑΛΜΑ στο {}: {}",
        "log_done":            "\n--- ΟΛΟΚΛΗΡΩΘΗΚΕ ---\n   Δημιουργήθηκαν: {}  |  Σφάλματα: {}",
        "language_label":      "Γλώσσα:"
    },
    "pt": {
        "window_title":        "Conversor MusicXML → MIDI",
        "btn_browse":          "Selecionar Pasta",
        "btn_start":           "INICIAR / ATUALIZAR",
        "btn_start_running":   "A executar …",
        "btn_stop":            "PARAR",
        "label_ready":         "Pronto para novas músicas",
        "label_ready2":        "Pronto para mais músicas",
        "config_info":         "Definições guardadas em: {}",
        "log_no_music21":      "⚠  AVISO: o music21 não está instalado!\n   Por favor execute:  pip install music21",
        "log_music21_ok":      "✓  music21 encontrado – pronto para a conversão.",
        "log_last_path":       "   Último caminho carregado: {}",
        "log_folder_chosen":   "   Pasta selecionada: {}",
        "log_new_scan":        "\n--- Nova verificação iniciada ---",
        "log_abort_req":       "   ⏹  Cancelamento solicitado …",
        "err_no_music21":      "ERRO: o music21 não está instalado!",
        "err_no_dir":          "ERRO: A pasta não existe: {}",
        "log_no_files":        "Nenhum ficheiro XML/MXL encontrado na pasta.",
        "progress_files":      "{} / {} ficheiros …",
        "log_aborted":         "   ⏹  Cancelado.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Plano B): {} recuperado.",
        "log_info_c":          "   INFO: {} – a usar o Plano C (apenas notas) …",
        "log_ok_c":            "✓  OK (Plano C): {} (apenas fluxo de notas)",
        "log_error_file":      "✗  ERRO em {}: {}",
        "log_done":            "\n--- CONCLUÍDO ---\n   Criados: {}  |  Erros: {}",
        "language_label":      "Idioma:"
    },
    "sv": {
        "window_title":        "MusicXML → MIDI Konverterare",
        "btn_browse":          "Välj mapp",
        "btn_start":           "STARTA / UPPDATERA",
        "btn_start_running":   "Körs …",
        "btn_stop":            "STOPP",
        "label_ready":         "Redo för nya låtar",
        "label_ready2":        "Redo for fler låtar",
        "config_info":         "Inställningar sparade i: {}",
        "log_no_music21":      "⚠  VARNING: music21 är inte installerat!\n   Kör vänligen:  pip install music21",
        "log_music21_ok":      "✓  music21 hittades – redo för konvertering.",
        "log_last_path":       "   Senaste sökväg laddad: {}",
        "log_folder_chosen":   "   Mapp vald: {}",
        "log_new_scan":        "\n--- Ny skanning startad ---",
        "log_abort_req":       "   ⏹  Avbrott begärt …",
        "err_no_music21":      "FEL: music21 är inte installerat!",
        "err_no_dir":          "FEL: Mappen finns inte: {}",
        "log_no_files":        "Inga XML/MXL-filer hittades i mappen.",
        "progress_files":      "{} / {} filer …",
        "log_aborted":         "   ⏹  Avbruten.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Plan B): {} räddad.",
        "log_info_c":          "   INFO: {} – använder Plan C (endast noter) …",
        "log_ok_c":            "✓  OK (Plan C): {} (endast notström)",
        "log_error_file":      "FEL på {}: {}",
        "log_done":            "\n--- KLAR ---\n   Skapade: {}  |  Fel: {}",
        "language_label":      "Språk:"
    },
    "hu": {
        "window_title":        "MusicXML → MIDI Konverteráló",
        "btn_browse":          "Mappa kiválasztása",
        "btn_start":           "INDÍTÁS / FRISSÍTÉS",
        "btn_start_running":   "Futás …",
        "btn_stop":            "LEÁLLÍTÁS",
        "label_ready":         "Készen áll az új dalokra",
        "label_ready2":        "Készen áll a további dalokra",
        "config_info":         "Beállítások elmentve ide: {}",
        "log_no_music21":      "⚠  FIGYELMEZTETÉS: a music21 nincs telepítve!\n   Kérjük, futtassa:  pip install music21",
        "log_music21_ok":      "✓  music21 megtalálva – készen áll a konvertálásra.",
        "log_last_path":       "   Legutóbbi útvonal betöltve: {}",
        "log_folder_chosen":   "   Kiválasztott mappa: {}",
        "log_new_scan":        "\n--- Új keresés elindítva ---",
        "log_abort_req":       "   ⏹  Megszakítás kérve …",
        "err_no_music21":      "HIBA: a music21 nincs telepítve!",
        "err_no_dir":          "HIBA: A mappa nem létezik: {}",
        "log_no_files":        "Nem találhatók XML/MXL fájlok a mappában.",
        "progress_files":      "{} / {} fájl …",
        "log_aborted":         "   ⏹  Megszakítva.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (B Terv): {} megmentve.",
        "log_info_c":          "   INFÓ: {} – C Terv használata (csak hangjegyek) …",
        "log_ok_c":            "✓  OK (C Terv): {} (csak hangjegy-folyam)",
        "log_error_file":      "✗  HIBA itt: {}: {}",
        "log_done":            "\n--- KÉSZ ---\n   Létrehozva: {}  |  Hiba: {}",
        "language_label":      "Nyelv:"
    },
    "ro": {
        "window_title":        "Convertor MusicXML → MIDI",
        "btn_browse":          "Selectează folderul",
        "btn_start":           "START / ACTUALIZARE",
        "btn_start_running":   "Rulează …",
        "btn_stop":            "STOP",
        "label_ready":         "Pregătit pentru melodii noi",
        "label_ready2":        "Pregătit pentru mai multe melodii",
        "config_info":         "Setări salvate în: {}",
        "log_no_music21":      "⚠  AVERTISMENT: music21 nu este instalat!\n   Vă rugăm să rulați:  pip install music21",
        "log_music21_ok":      "✓  music21 a fost găsit – pregătit pentru conversie.",
        "log_last_path":       "   Ultima cale încărcată: {}",
        "log_folder_chosen":   "   Folder selectat: {}",
        "log_new_scan":        "\n--- Scanare nouă pornită ---",
        "log_abort_req":       "   ⏹  Anulare solicitată …",
        "err_no_music21":      "EROARE: music21 nu este instalat!",
        "err_no_dir":          "EROARE: Folderul nu există: {}",
        "log_no_files":        "Nu s-au găsit fișiere XML/MXL în folder.",
        "progress_files":      "{} / {} fișiere …",
        "log_aborted":         "   ⏹  Anulat.",
        "log_ok":              "✓  OK: {}",
        "log_ok_b":            "✓  OK (Planul B): {} salvat.",
        "log_info_c":          "   INFO: {} – se utilizează Planul C (doar note) …",
        "log_ok_c":            "✓  OK (Planul C): {} (doar flux de note)",
        "log_error_file":      "✗  EROARE la {}: {}",
        "log_done":            "\n--- GATA ---\n   Create: {}  |  Erori: {}",
        "language_label":      "Limbă:"
    },
}

LANGUAGE_OPTIONS = {
    "Deutsch":       "de",
    "English":       "en",
    "Français":      "fr",
    "Español":       "es",
    "Italiano":      "it",
    "Nederlands":    "nl",
    "Polski":        "pl",
    "Čeština":       "cs",
    "Русский":       "ru",
    "Українська":    "uk",
    "Türkçe":        "tr",
    "Ελληνικά":      "el",
    "Português":     "pt",
    "Svenska":       "sv",
    "Magyar":        "hu",
    "Română":        "ro",
}

# ──────────────────────────────────────────────
#  Plattform-Helfer
# ──────────────────────────────────────────────

def get_desktop_path() -> str:
    return os.path.join(os.path.expanduser("~"), "Desktop")


def get_config_dir() -> str:
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config"))
    config_dir = os.path.join(base, APP_NAME)
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def get_config_file() -> str:
    return os.path.join(get_config_dir(), "settings.json")


def load_settings() -> dict:
    """Lädt alle gespeicherten Einstellungen. Fallback auf Defaults."""
    try:
        with open(get_config_file(), "r", encoding="utf-8") as f:
            data = json.load(f)
            path = data.get("last_path", "")
            if path and not os.path.isdir(path):
                data["last_path"] = ""
            return data
    except Exception:
        pass
    desktop = get_desktop_path()
    return {
        "last_path": desktop if os.path.isdir(desktop) else os.path.expanduser("~"),
        "language":  "de",
    }


def save_settings(path: str, language: str) -> None:
    try:
        with open(get_config_file(), "w", encoding="utf-8") as f:
            json.dump({"last_path": path, "language": language}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ──────────────────────────────────────────────
#  Haupt-App
# ──────────────────────────────────────────────

class ConverterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.resizable(True, True)
        self._stop_flag = threading.Event()

        settings = load_settings()
        self._lang_code = settings.get("language", "de")
        self._last_path = settings.get("last_path", get_desktop_path())

        self._build_scrollable_window()
        self.setup_gui()
        self._load_icon()

    # ── Übersetzungs-Helfer ────────────────────
    def t(self, key: str, *args) -> str:
        """Gibt den übersetzten String zurück, optional mit .format()-Werten."""
        text = TRANSLATIONS.get(self._lang_code, TRANSLATIONS["de"]).get(key, key)
        return text.format(*args) if args else text

    # ── Sprache wechseln ───────────────────────
    def _on_language_change(self, *_):
        display_name = self._lang_var.get()
        new_code     = LANGUAGE_OPTIONS.get(display_name, "de")
        if new_code == self._lang_code:
            return
        self._lang_code = new_code
        save_settings(self.path_var.get(), self._lang_code)
        self._apply_translations()

    def _apply_translations(self):
        """Aktualisiert alle UI-Texte nach einem Sprachwechsel."""
        self.root.title(self.t("window_title"))
        self._btn_browse.config(text=self.t("btn_browse"))
        self.btn_start.config(text=self.t("btn_start"))
        self.btn_stop.config(text=self.t("btn_stop"))
        self.progress_label.config(text=self.t("label_ready"))
        self._lang_label.config(text=self.t("language_label"))
        self._config_info_label.config(text=self.t("config_info", get_config_dir()))

    # ── Icon laden ─────────────────────────────
    def _load_icon(self):
        """
        Setzt das Fenster-Icon.
        Sucht icon.ico / icon.png im selben Ordner wie das Skript.
        Kein Fehler wenn nicht gefunden – Icon ist optional.
        """
        base = os.path.dirname(os.path.abspath(__file__))
        try:
            ico = os.path.join(base, "icon.ico")
            if os.path.isfile(ico):
                self.root.iconbitmap(ico)
                return
        except Exception:
            pass
        try:
            png = os.path.join(base, "icon.png")
            if os.path.isfile(png):
                img = tk.PhotoImage(file=png)
                self.root.iconphoto(True, img)
        except Exception:
            pass

    # ── Scrollbares Hauptfenster ───────────────
    def _build_scrollable_window(self):
        outer = tk.Frame(self.root)
        outer.pack(fill=tk.BOTH, expand=True)

        self._scrollbar = tk.Scrollbar(outer, orient=tk.VERTICAL)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._canvas = tk.Canvas(outer, yscrollcommand=self._scrollbar.set,
                                 highlightthickness=0)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._scrollbar.config(command=self._canvas.yview)

        self.main_frame = tk.Frame(self._canvas)
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self.main_frame, anchor="nw"
        )

        self.main_frame.bind("<Configure>", self._on_frame_configure)
        self._canvas.bind("<Configure>",    self._on_canvas_configure)
        self._canvas.bind("<Enter>",        self._bind_mousewheel)
        self._canvas.bind("<Leave>",        self._unbind_mousewheel)

    def _on_frame_configure(self, _=None):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self._canvas.itemconfig(self._canvas_window, width=event.width)

    def _bind_mousewheel(self, _=None):
        if sys.platform == "win32":
            self._canvas.bind_all("<MouseWheel>", self._on_mousewheel_win)
        elif sys.platform == "darwin":
            self._canvas.bind_all("<MouseWheel>", self._on_mousewheel_mac)
        else:
            self._canvas.bind_all("<Button-4>", self._on_mousewheel_linux_up)
            self._canvas.bind_all("<Button-5>", self._on_mousewheel_linux_down)

    def _unbind_mousewheel(self, _=None):
        if sys.platform == "win32":
            self._canvas.unbind_all("<MouseWheel>")
        elif sys.platform == "darwin":
            self._canvas.unbind_all("<MouseWheel>")
        else:
            self._canvas.unbind_all("<Button-4>")
            self._canvas.unbind_all("<Button-5>")

    def _on_mousewheel_win(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_mac(self, event):
        self._canvas.yview_scroll(int(-1 * event.delta), "units")

    def _on_mousewheel_linux_up(self, _):
        self._canvas.yview_scroll(-1, "units")

    def _on_mousewheel_linux_down(self, _):
        self._canvas.yview_scroll(1, "units")

    # ── GUI-Aufbau ─────────────────────────────
    def setup_gui(self):
        self.root.title(self.t("window_title"))
        self.root.geometry("620x520")
        self.root.minsize(500, 380)

        # ── Sprachauswahl ──
        lang_frame = tk.Frame(self.main_frame)
        lang_frame.pack(pady=(10, 0), fill=tk.X, padx=10)

        self._lang_label = tk.Label(lang_frame, text=self.t("language_label"), font=("TkDefaultFont", 9))
        self._lang_label.pack(side=tk.LEFT)

        # Anzeigename der aktuellen Sprache ermitteln
        current_display = next(
            (k for k, v in LANGUAGE_OPTIONS.items() if v == self._lang_code),
            "Deutsch"
        )
        self._lang_var = tk.StringVar(value=current_display)
        lang_menu = ttk.Combobox(
            lang_frame,
            textvariable=self._lang_var,
            values=list(LANGUAGE_OPTIONS.keys()),
            state="readonly",
            width=14,
        )
        lang_menu.pack(side=tk.LEFT, padx=5)
        self._lang_var.trace_add("write", self._on_language_change)

        # ── Pfad-Auswahl ──
        top_frame = tk.Frame(self.main_frame)
        top_frame.pack(pady=8, fill=tk.X, padx=10)

        self.path_var = tk.StringVar(value=self._last_path)
        tk.Entry(top_frame, textvariable=self.path_var).pack(
            side=tk.LEFT, expand=True, fill=tk.X)
        self._btn_browse = tk.Button(
            top_frame, text=self.t("btn_browse"), command=self.browse_folder)
        self._btn_browse.pack(side=tk.LEFT, padx=5)

        # ── Buttons ──
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(pady=5)

        self.btn_start = tk.Button(
            btn_frame, text=self.t("btn_start"),
            bg="green", fg="white", font=("TkDefaultFont", 10, "bold"),
            command=self.start_thread,
        )
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_stop = tk.Button(
            btn_frame, text=self.t("btn_stop"),
            state="disabled", command=self.stop_conversion,
        )
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        # ── Fortschritt ──
        self.progress_label = tk.Label(self.main_frame, text=self.t("label_ready"))
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(self.main_frame, mode="determinate")
        self.progress_bar.pack(pady=5, fill=tk.X, padx=10)

        # ── Konfig-Pfad anzeigen ──
        self._config_info_label = tk.Label(
            self.main_frame,
            text=self.t("config_info", get_config_dir()),
            fg="gray", font=("Arial", 8),
        )
        self._config_info_label.pack()

        # ── Log ──
        self.log_area = scrolledtext.ScrolledText(self.main_frame, height=18, font=("TkFixedFont", 10))
        self.log_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # Status-Meldungen beim Start
        if not MUSIC21_AVAILABLE:
            self.log_msg(self.t("log_no_music21"))
        else:
            self.log_msg(self.t("log_music21_ok"))
        self.log_msg(self.t("log_last_path", self.path_var.get()))

    # ── Aktionen ───────────────────────────────
    def browse_folder(self):
        current = self.path_var.get()
        start   = current if os.path.isdir(current) else os.path.expanduser("~")
        d = filedialog.askdirectory(initialdir=start)
        if d:
            self.path_var.set(d)
            save_settings(d, self._lang_code)
            self.log_msg(self.t("log_folder_chosen", d))

    def log_msg(self, msg: str):
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)

    def ui(self, fn):
        self.root.after(0, fn)

    def start_thread(self):
        self._stop_flag.clear()
        self.progress_bar["value"] = 0
        self.log_msg(self.t("log_new_scan"))
        save_settings(self.path_var.get(), self._lang_code)
        threading.Thread(target=self.run_conversion, daemon=True).start()

    def stop_conversion(self):
        self._stop_flag.set()
        self.log_msg(self.t("log_abort_req"))

    def _set_running(self, running: bool):
        if running:
            self.btn_start.config(state="disabled", text=self.t("btn_start_running"))
            self.btn_stop.config(state="normal")
        else:
            self.btn_start.config(state="normal", text=self.t("btn_start"))
            self.btn_stop.config(state="disabled")

    # ── Konvertierung ──────────────────────────
    def run_conversion(self):
        if not MUSIC21_AVAILABLE:
            self.ui(lambda: self.log_msg(self.t("err_no_music21")))
            return

        source_dir = self.path_var.get()
        if not os.path.isdir(source_dir):
            self.ui(lambda: self.log_msg(self.t("err_no_dir", source_dir)))
            return

        files = [
            os.path.join(dp, f)
            for dp, _, filenames in os.walk(source_dir)
            for f in filenames
            if f.lower().endswith(SUPPORTED_EXT)
        ]

        if not files:
            self.ui(lambda: self.log_msg(self.t("log_no_files")))
            return

        total = len(files)
        self.ui(lambda: self._set_running(True))
        self.ui(lambda: self.progress_bar.config(maximum=total, value=0))
        self.ui(lambda: self.progress_label.config(text=self.t("progress_files", 0, total)))

        created, errors = 0, 0

        for i, src in enumerate(files):
            if self._stop_flag.is_set():
                self.ui(lambda: self.log_msg(self.t("log_aborted")))
                break

            filename  = os.path.basename(src)
            midi_path = os.path.splitext(src)[0] + ".mid"

            self.ui(lambda v=i: self.progress_bar.config(value=v + 1))
            self.ui(lambda v=i: self.progress_label.config(
                text=self.t("progress_files", v + 1, total)))

            try:
                score = converter.parse(src)

                # Plan A
                try:
                    score.write("midi", fp=midi_path)
                    created += 1
                    self.ui(lambda fn=filename: self.log_msg(self.t("log_ok", fn)))

                except Exception:
                    # Plan B
                    for part in score.parts:
                        part.removeByClass(["Repeat", "Ending", "Coda", "Segno", "Mark"])
                        for m in part.getElementsByClass("Measure"):
                            m.leftBarline  = None
                            m.rightBarline = None
                    try:
                        score.write("midi", fp=midi_path)
                        created += 1
                        self.ui(lambda fn=filename: self.log_msg(self.t("log_ok_b", fn)))

                    except Exception:
                        # Plan C
                        self.ui(lambda fn=filename: self.log_msg(self.t("log_info_c", fn)))
                        nackte_noten = score.flat.notesAndRests
                        nackte_noten.write("midi", fp=midi_path)
                        created += 1
                        self.ui(lambda fn=filename: self.log_msg(self.t("log_ok_c", fn)))

            except Exception as e:
                errors += 1
                err_msg = str(e)
                self.ui(lambda fn=filename, em=err_msg:
                        self.log_msg(self.t("log_error_file", fn, em)))

        self.ui(lambda: self.log_msg(self.t("log_done", created, errors)))
        self.ui(lambda: self._set_running(False))
        self.ui(lambda: self.progress_label.config(text=self.t("label_ready2")))
        save_settings(self.path_var.get(), self._lang_code)


if __name__ == "__main__":
    root = tk.Tk()
    app  = ConverterApp(root)
    root.mainloop()
