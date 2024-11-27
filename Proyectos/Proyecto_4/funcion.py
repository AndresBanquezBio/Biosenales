import scipy.signal as sis
import pywt
import numpy as np

def filtro_wavelet_modificado(senal, wavelet_type='db6', nivel=8):
    '''
    Filtra la señal usando una descomposición wavelet y reconstrucción, permitiendo
    seleccionar diferentes tipos de wavelet (db6, sym3, coif3, meyer, etc.).

    Parámetros:
    - senal: np.array, señal de entrada a filtrar.
    - wavelet_type: str, tipo de wavelet a utilizar (por defecto 'db6').
    - nivel: int, nivel de descomposición de la wavelet.

    Retorna:
    - Señal reconstruida después del filtrado wavelet.
    '''
    senal= senal.flatten()
    coeficientes = pywt.wavedec(senal, wavelet=wavelet_type, level=nivel)
    
    # Aplicar umbral a los coeficientes de detalle
    sigma = np.median(np.abs(coeficientes[-1])) / 0.6745
    umbral = sigma * np.sqrt(2 * np.log(len(senal)))
    coeficientes_filtrados = [pywt.threshold(c, umbral, mode='soft') for c in coeficientes]
    
    # Reconstruir la señal
    senal_filtrada = pywt.waverec(coeficientes_filtrados, wavelet=wavelet_type)
    return senal_filtrada

def filtro_pasa_altas(data, fs, cutoff=0.5, order=1650):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b,a = sis.firwin(order+1, normal_cutoff, pass_zero = 'highpass', window = 'hamming'),1
    return sis.filtfilt(b, a, data)


def filtro_pasa_bajas(data, fs, cutoff=50, order=1650):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b,a = sis.firwin(order+1, normal_cutoff, pass_zero = 'lowpass', window = 'hamming'),1
    return sis.filtfilt(b, a, data)

def flujo_1(data, fs):
    data_hp = filtro_pasa_altas(data, fs)
    data_wavelet = filtro_wavelet_modificado(data_hp)
    data_lp = filtro_pasa_bajas(data_wavelet, fs)
    return data_lp