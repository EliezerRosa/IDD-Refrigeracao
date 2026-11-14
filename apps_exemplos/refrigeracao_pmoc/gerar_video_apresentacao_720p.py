"""Gera capturas reais da UI, locução neural em dueto e vídeo MP4 720p (1280x720)
da apresentação completa do protótipo RefriFácil (IDD Refrigeração Ágil).
"""

import argparse
import asyncio
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import edge_tts
import numpy as np
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT_DIR = Path(r"C:\Antigravity - IDD Refrigeração")
APP_DIR = ROOT_DIR / "apps_exemplos" / "refrigeracao_pmoc"
APRESENTACAO_DIR = ROOT_DIR / "apresentacao"
BUILD_DIR = ROOT_DIR / "outputs" / "refrifacil_720p_build"
UI_SHOTS_DIR = BUILD_DIR / "ui_shots"
AUDIO_DIR = BUILD_DIR / "audio"

APP_HTML = APP_DIR / "app_refrigeracao.html"
PRES_HTML = APP_DIR / "apresentacao_prototipo_refrifacil.html"
PRES_HTML_COPY = APRESENTS_COPY = APRESENTACAO_DIR / "apresentacao_prototipo_refrifacil.html"

MASTER_WAV = BUILD_DIR / "master_audio_refrifacil.wav"
TIMELINE_JSON = BUILD_DIR / "timeline_refrifacil.json"

FINAL_MP4_APP = APP_DIR / "Apresentacao_Prototipo_RefriFacil_720p.mp4"
FINAL_MP4_APRES = APRESENTACAO_DIR / "Apresentacao_Prototipo_RefriFacil_720p.mp4"

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

VOICE_APRESENTADORA = "pt-BR-FranciscaNeural"
VOICE_ARQUITETO = "pt-BR-AntonioNeural"

SCRIPT_LINES = [
    # SLIDE 1: O Novo Escopo Enxuto
    {
        "index": 0,
        "speaker": "leigo",
        "actor": "Apresentadora",
        "who": "leigo",
        "voice": VOICE_APRESENTADORA,
        "slide": 1,
        "text": "Bem-vindos à apresentação completa do RefriFácil, o protótipo da nova proposta IDD Refrigeração Ágil! Eliézer, por que reduzimos drasticamente a complexidade industrial para focar no atendimento doméstico e em pequenos negócios?"
    },
    {
        "index": 1,
        "speaker": "eliezer",
        "actor": "Eliézer Rosa",
        "who": "eliezer",
        "voice": VOICE_ARQUITETO,
        "slide": 1,
        "text": "Porque o técnico autônomo e a pequena assistência não vivem de laudos burocráticos complexos. Eles precisam atender rápido o Split residencial, o balcão de carnes do açougue, o expositor do bar e o freezer da padaria, sem perder tempo no celular!"
    },
    # SLIDE 2: MER Canônico de 3 Tabelas (schema.sql)
    {
        "index": 2,
        "speaker": "leigo",
        "actor": "Apresentadora",
        "who": "leigo",
        "voice": VOICE_APRESENTADORA,
        "slide": 2,
        "text": "E essa simplicidade começa direto no banco de dados! No Slide dois vemos que o arquivo schema ponto sql foi enxugado para apenas três tabelas essenciais. Como ficou essa estrutura?"
    },
    {
        "index": 3,
        "speaker": "eliezer",
        "actor": "Eliézer Rosa",
        "who": "eliezer",
        "voice": VOICE_ARQUITETO,
        "slide": 2,
        "text": "Exato! Temos apenas Clientes, Equipamentos e Ordens de Serviço. Na OS gravamos a leitura prática de termômetro e manômetro, somamos peças e mão de obra automaticamente em valor total, e já garantimos por padrão os noventa dias de garantia do CDC!"
    },
    # SLIDE 3: Regras de Domínio & Mínimo Legal CDC (domain_rules.ts)
    {
        "index": 4,
        "speaker": "leigo",
        "actor": "Apresentadora",
        "who": "leigo",
        "voice": VOICE_APRESENTADORA,
        "slide": 3,
        "text": "No Slide três entramos no coração de invariantes em domain rules ponto ts. Como a máquina de estados e o mínimo legal obrigatório protegem tanto o técnico quanto o cliente sem gerar atrito?"
    },
    {
        "index": 5,
        "speaker": "eliezer",
        "actor": "Eliézer Rosa",
        "who": "eliezer",
        "voice": VOICE_ARQUITETO,
        "slide": 3,
        "text": "O fluxo tem só três passos claros: Aberta, Em Andamento e Concluída. Nenhuma ordem fecha sem relato técnico e valores válidos, assegurando recibo transparente e o cumprimento automático da garantia legal de noventa dias do artigo vinte e seis do CDC!"
    },
    # SLIDE 4: Abertura Ágil de OS (Aba 1: Chamados de Campo)
    {
        "index": 6,
        "speaker": "leigo",
        "actor": "Apresentadora",
        "who": "leigo",
        "voice": VOICE_APRESENTADORA,
        "slide": 4,
        "text": "Agora vamos à tela real do protótipo no Slide quatro! Na primeira aba, Chamados de Campo, como funciona a abertura rápida de uma ordem de serviço e os indicadores no topo?"
    },
    {
        "index": 7,
        "speaker": "eliezer",
        "actor": "Eliézer Rosa",
        "who": "eliezer",
        "voice": VOICE_ARQUITETO,
        "slide": 4,
        "text": "No topo acompanhamos visitas aguardando, em execução, faturamento e garantias. Ao escolher Residencial ou Pequeno Comércio, o sistema adapta na hora a lista de aparelhos e a estimativa de mão de obra de cento e oitenta para duzentos e cinquenta reais!"
    },
    # SLIDE 5: Fechamento em Campo, Recibo & WhatsApp
    {
        "index": 8,
        "speaker": "leigo",
        "actor": "Apresentadora",
        "who": "leigo",
        "voice": VOICE_APRESENTADORA,
        "slide": 5,
        "text": "E quando o técnico termina o reparo no cliente? No Slide cinco vemos o modal de conclusão e geração de recibo. O que acontece ao finalizar?"
    },
    {
        "index": 9,
        "speaker": "eliezer",
        "actor": "Eliézer Rosa",
        "who": "eliezer",
        "voice": VOICE_ARQUITETO,
        "slide": 5,
        "text": "O técnico preenche o serviço executado, a temperatura de saída, a pressão em PSI, peças e forma de pagamento como PIX ou Cartão. Com um clique, o app gera a mensagem completa com garantia de noventa dias direto no WhatsApp do cliente e libera impressão física!"
    },
    # SLIDE 6: Equipamentos & Pequenos Negócios (Aba 2)
    {
        "index": 10,
        "speaker": "leigo",
        "actor": "Apresentadora",
        "who": "leigo",
        "voice": VOICE_APRESENTADORA,
        "slide": 6,
        "text": "No Slide seis destacamos a segunda aba do sistema: Equipamentos e Negócios. Por que essa visão separada é estratégica para o refrigerista que atende o comércio do bairro?"
    },
    {
        "index": 11,
        "speaker": "eliezer",
        "actor": "Eliézer Rosa",
        "who": "eliezer",
        "voice": VOICE_ARQUITETO,
        "slide": 6,
        "text": "Porque quando um balcão de carnes ou expositor de bebidas falha, o comerciante perde estoque perecível na hora! Aqui o técnico enxerga todo o parque comercial atendido, com histórico e WhatsApp rápido para preventivas recorrentes!"
    },
    # SLIDE 7: Termômetro & Diagnóstico Rápido de Bolso (Aba 3)
    {
        "index": 12,
        "speaker": "leigo",
        "actor": "Apresentadora",
        "who": "leigo",
        "voice": VOICE_APRESENTADORA,
        "slide": 7,
        "text": "E na terceira aba, apresentada no Slide sete, temos a ferramenta de Termômetro e Diagnóstico! Como ela ajuda o técnico na frente do cliente sem complicação matemática?"
    },
    {
        "index": 13,
        "speaker": "eliezer",
        "actor": "Eliézer Rosa",
        "who": "eliezer",
        "voice": VOICE_ARQUITETO,
        "slide": 7,
        "text": "Basta digitar a temperatura de retorno, a saída de ar e a pressão em PSI para gases como R410A, R32 ou R134a. Se o Delta T ficar entre dez e dezesseis graus, o app confirma rendimento ótimo; abaixo de oito graus, alerta na hora para filtro sujo ou falta de gás!"
    },
    # SLIDE 8: Faturamento, Garantias CDC & Modo Offline-First (Aba 4)
    {
        "index": 14,
        "speaker": "leigo",
        "actor": "Apresentadora",
        "who": "leigo",
        "voice": VOICE_APRESENTADORA,
        "slide": 8,
        "text": "Fechando no Slide oito, vemos a aba Faturamento e Garantias e o próximo passo para testes da interface. O que o gestor ou autônomo controla aqui?"
    },
    {
        "index": 15,
        "speaker": "eliezer",
        "actor": "Eliézer Rosa",
        "who": "eliezer",
        "voice": VOICE_ARQUITETO,
        "slide": 8,
        "text": "Ele separa exatamente o lucro de mão de obra do repasse de peças, vê o ticket médio e consulta cada garantia ativa de noventa dias com reenvio instantâneo no WhatsApp. Tudo persistido localmente no navegador, pronto para testarmos cada clique da UI!"
    }
]


def capture_ui_screenshots() -> dict:
    """Captura 5 telas reais da UI app_refrigeracao.html em outputs/refrifacil_720p_build/ui_shots/."""
    UI_SHOTS_DIR.mkdir(parents=True, exist_ok=True)
    if not APP_HTML.exists():
        raise FileNotFoundError(f"Protótipo HTML não encontrado: {APP_HTML}")

    shots = {
        "tab1": UI_SHOTS_DIR / "ui_tab1_chamados.png",
        "modal": UI_SHOTS_DIR / "ui_modal_conclusao.png",
        "tab2": UI_SHOTS_DIR / "ui_tab2_equipamentos.png",
        "tab3": UI_SHOTS_DIR / "ui_tab3_diagnostico.png",
        "tab4": UI_SHOTS_DIR / "ui_tab4_faturamento.png",
    }

    print("=" * 72)
    print("📸 [PASSO 1] CAPTURANDO TELAS REAIS DO PROTÓTIPO (app_refrigeracao.html)")
    print("=" * 72)

    file_url = "file:///" + str(APP_HTML).replace("\\", "/")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=CHROME_PATH,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--allow-file-access-from-files"],
        )
        page = browser.new_page(viewport={"width": 1280, "height": 800}, device_scale_factor=1)
        page.goto(file_url, wait_until="domcontentloaded")
        page.wait_for_timeout(1200)

        # 1. Aba 1 - Chamados de Campo
        page.screenshot(path=str(shots["tab1"]))
        print(f"  ✓ {shots['tab1'].name}")

        # 2. Modal de Conclusão (OS-201)
        page.evaluate("abrirModalConclusao('OS-201')")
        page.wait_for_timeout(400)
        page.screenshot(path=str(shots["modal"]))
        print(f"  ✓ {shots['modal'].name}")

        # 3. Aba 2 - Equipamentos & Negócios
        page.evaluate("fecharModal(); switchView('equip')")
        page.wait_for_timeout(400)
        page.screenshot(path=str(shots["tab2"]))
        print(f"  ✓ {shots['tab2'].name}")

        # 4. Aba 3 - Termômetro & Diagnóstico
        page.evaluate("switchView('diag')")
        page.wait_for_timeout(400)
        page.screenshot(path=str(shots["tab3"]))
        print(f"  ✓ {shots['tab3'].name}")

        # 5. Aba 4 - Faturamento & Garantias
        page.evaluate("switchView('relatorio')")
        page.wait_for_timeout(400)
        page.screenshot(path=str(shots["tab4"]))
        print(f"  ✓ {shots['tab4'].name}")

        browser.close()

    return shots


def embed_screenshots_into_html(shots: dict) -> None:
    """Injeta Data URIs base64 das capturas no HTML da apresentação (e copia para apresentacao/)."""
    if not PRES_HTML.exists():
        raise FileNotFoundError(f"HTML da apresentação não encontrado: {PRES_HTML}")

    html = PRES_HTML.read_text(encoding="utf-8")
    for key, path in shots.items():
        token = f"{{{{SHOT_{key.upper()}}}}}"
        b64 = base64.b64encode(path.read_bytes()).decode("ascii")
        data_uri = f"data:image/png;base64,{b64}"
        if token in html:
            html = html.replace(token, data_uri)

    PRES_HTML.write_text(html, encoding="utf-8")
    APRESENTACAO_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PRES_HTML, PRES_HTML_COPY)
    print(f"  ✓ Data URIs injetados em {PRES_HTML.name} e copiado para apresentacao/")


async def gen_tts_file(text: str, voice: str, out_wav: Path) -> None:
    communicate = edge_tts.Communicate(text, voice)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        await communicate.save(str(tmp_path))
        cmd = [
            "ffmpeg", "-y",
            "-i", str(tmp_path),
            "-ar", "48000",
            "-ac", "1",
            str(out_wav),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def get_wav_duration_and_samples(wav_path: Path):
    with wave.open(str(wav_path), "rb") as wf:
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        frames = wf.readframes(n_frames)
        dur = n_frames / framerate
        samples = np.frombuffer(frames, dtype=np.int16)
        return dur, samples, framerate


async def build_audio_and_timeline() -> dict:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    print("\n" + "=" * 72)
    print("🎙️ [PASSO 3A] SINTETIZANDO LOCUÇÃO NEURAL EM DUETO (edge_tts)")
    print("=" * 72)

    timeline_items = []
    all_audio_segments = []
    rate = 48000

    # 0.8s de respiro inicial
    lead_silence = np.zeros(int(rate * 0.8), dtype=np.int16)
    all_audio_segments.append(lead_silence)
    current_time = 0.8

    for item in SCRIPT_LINES:
        idx = item["index"]
        out_wav = AUDIO_DIR / f"seg_{idx:02d}_{item['speaker']}.wav"
        print(f"  [{idx + 1:02d}/{len(SCRIPT_LINES):02d}] {item['actor']} (Slide {item['slide']})...")
        await gen_tts_file(item["text"], item["voice"], out_wav)

        dur, samples, rate = get_wav_duration_and_samples(out_wav)
        start_sec = current_time
        end_sec = current_time + dur

        timeline_items.append({
            "index": idx,
            "speaker": item["speaker"],
            "actor": item["actor"],
            "who": item["who"],
            "slide": item["slide"],
            "text": item["text"],
            "startSec": round(start_sec, 3),
            "endSec": round(end_sec, 3),
            "durationSec": round(dur, 3),
        })

        all_audio_segments.append(samples)
        pause_samples = np.zeros(int(rate * 0.40), dtype=np.int16)
        all_audio_segments.append(pause_samples)
        current_time = end_sec + 0.40

    # 1.4s de silêncio final
    tail_silence = np.zeros(int(rate * 1.4), dtype=np.int16)
    all_audio_segments.append(tail_silence)
    final_audio = np.concatenate(all_audio_segments)

    with wave.open(str(MASTER_WAV), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(final_audio.tobytes())

    total_dur = len(final_audio) / rate
    timeline_data = {
        "title": "RefriFácil — Apresentação Completa do Protótipo IDD Refrigeração Ágil",
        "totalDurationSec": round(total_dur, 2),
        "items": timeline_items,
    }
    TIMELINE_JSON.write_text(json.dumps(timeline_data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"  ✓ Áudio master: {MASTER_WAV.name} ({total_dur:.2f}s / ~{total_dur/60:.2f} min)")
    print(f"  ✓ Timeline salva: {TIMELINE_JSON.name}")
    return timeline_data


def render_mp4_720p(timeline_data: dict) -> None:
    print("\n" + "=" * 72)
    print("🎬 [PASSO 3B] RENDERIZANDO VÍDEO MP4 720p (1280x720 @ 30fps CFR)")
    print("=" * 72)

    total_dur = float(timeline_data["totalDurationSec"])
    fps = 5
    total_frames = int(np.ceil(total_dur * fps))
    temp_out = BUILD_DIR / "temp_refrifacil_720p.mp4"
    if temp_out.exists():
        temp_out.unlink()

    file_url = "file:///" + str(PRES_HTML).replace("\\", "/")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=CHROME_PATH,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--allow-file-access-from-files",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
            ],
        )
        page = browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
        page.goto(file_url, wait_until="domcontentloaded")
        page.wait_for_timeout(1500)

        page.evaluate(
            "(payload) => { if (window.setTimeline) window.setTimeline(payload.items, payload.totalDurationSec); }",
            {"items": timeline_data["items"], "totalDurationSec": total_dur},
        )

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-f", "image2pipe",
            "-c:v", "mjpeg",
            "-r", str(fps),
            "-i", "pipe:0",
            "-i", str(MASTER_WAV),
            "-filter_complex", "[0:v]fps=30,scale=1280:720[v]",
            "-map", "[v]",
            "-map", "1:a:0",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "48000",
            "-shortest",
            "-movflags", "+faststart",
            str(temp_out),
        ]

        proc = subprocess.Popen(
            ffmpeg_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

        progress_step = max(1, total_frames // 20)
        for f in range(total_frames):
            t_sec = f / fps
            page.evaluate("(t) => window.updateFrameAtTime(t)", t_sec)
            buf = page.screenshot(
                type="jpeg",
                quality=90,
                clip={"x": 0, "y": 0, "width": 1280, "height": 720},
            )
            proc.stdin.write(buf)
            if f % progress_step == 0 or f == total_frames - 1:
                pct = ((f + 1) / total_frames) * 100
                print(f"  Frame {f + 1}/{total_frames} ({pct:.1f}%)")

        proc.stdin.close()
        stderr_bytes = proc.stderr.read()
        ret = proc.wait()
        browser.close()

        if ret != 0:
            raise RuntimeError(f"FFmpeg falhou com código {ret}:\n{stderr_bytes.decode('utf-8', errors='replace')}")

    shutil.copy2(temp_out, FINAL_MP4_APP)
    shutil.copy2(temp_out, FINAL_MP4_APRES)
    if temp_out.exists():
        temp_out.unlink()

    size_mb = FINAL_MP4_APP.stat().st_size / (1024 * 1024)
    print(f"  🎉 MP4 720p gerado: {FINAL_MP4_APP} ({size_mb:.2f} MB)")
    print(f"  🎉 Cópia salva em: {FINAL_MP4_APRES}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-only", action="store_true", help="Apenas captura as 5 telas reais da UI")
    args = parser.parse_args()

    shots = capture_ui_screenshots()
    if args.capture_only:
        print("Captura concluída (--capture-only).")
        return

    embed_screenshots_into_html(shots)
    timeline_data = asyncio.run(build_audio_and_timeline())
    render_mp4_720p(timeline_data)


if __name__ == "__main__":
    main()
