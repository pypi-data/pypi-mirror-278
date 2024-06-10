import logging
import threading
import types
import time
import concurrent.futures as cr
from datetime import timedelta, datetime
from functools import partial
from statistics import mean

from jsonmerge import merge
from python_flux.flux_utilis import FluxUtils as fu
from python_flux.subscribers import SSubscribe


class Flux(object):

    def filter(self, predicate, on_mismatch=fu.default_action):
        """
        Permite filtrar un flujo perimtiendo continuar a aquellos valores que cumplen con el
        predicado que se indica.
        Si no se cumple el predicado opcionalmente se puede indicar una función que dado el valor y el contexto acutal
        retorna el valor que se enviará al flujo.

        :param predicate: función(valor, contexto) que retorna un booleano
        :param on_mismatch: función(valor, contexto) que retorna un valor alternativo al testeado originalmente
        """
        return FFilter(predicate, on_mismatch, self)

    def map(self, map_function):
        """
        Permite modificar el valor de un flujo.
        Recibe una función(valor, contexto) que se evaluará para cada elemento del flujo y se substiuirá en el mismo
        por le obtenido de la función.

        :param map_function: función(valor, contexto) desde donde se obtendrá el valor a subsituir.
        """
        return FMap(map_function, self)

    def map_if(self, predicate, map_function):
        """
        Evalúa el predicado, si este es verdadero mapea el valor actual utilizando la función de mapeo.

        :param predicate: función(valor, contexto) predicado que se evalúa.
        :param map_function: función(valor, contexto) desde donde se obtendrá el valor a subsituir.
        """
        return FMapIf(predicate, map_function, self)

    def map_context(self, map_context_function):
        """
        Permite modificar el contexto de un flujo.
        Recibe una función(valor, contexto) que se evaluará para cada elemento del flujo y retornará
        un nuevo contexto que subsituirá al actual

        :param map_context_function: función(valor, contexto) desde donde se obtendrá el contexto a subsituir.
        """
        return FMapContext(map_context_function, self)

    def flat_map(self, flatmap_function):
        """
        Permite sustituir el valor de un flujo por elementos de otro flujo.
        Recibe una función(valor, contexto) que se evaluará para cada elemento del flujo original y retornará un
        flujo cuyos elementos se usarán como nuevo origen del flujo de datos.

        flatmap_function: función(valor, contexto) desde donde se obtendrá el valor a subsituir.
        """
        return FFlatMap(flatmap_function, self)

    def do_on_next(self, on_next, on_error=fu.default_action, exec_async=True):
        """
        Ejecuta par cada elemento del flujo una acción de forma asincrónica. No afecta a los valores
        del flujo.

        :param on_next: función(valor, contexto) se ejecuta para cada valor del flujo
        :param on_error: función(ex, contexto) se ejecuta en caso de error
        :param exec_async: Booleano que indica si las funciones se ejecutarán de forma asíncrona
        """
        return FDoOnNext(on_next, on_error, exec_async, self)

    def delay_ms(self, delay_ms, predicate=fu.default_predicate):
        """
        Retrasa en delay milisegundos la ejecución de paso del flujo. Esto marca el tiempo en que
        se procesarán sus elementos.

        :param delay_ms: Delay en milisegundos que se retrasará el procesamiento de los elementos del flujo
        :param predicate: Si es verdadero se aplica el delay establecido
        """
        return FDelayMs(delay_ms, predicate, self)

    def rate(self, rate, must_apply=fu.default_predicate):
        """
        Fuerza un flujo constante de procesamiento de elementos en el stream.
        Para esto una vez fijado el rate de procesamiento en RPS, se mide el tiempo de producción
        de cada elemento y si este es inerior al indicado por el rate se espera el tiempo suficiente para asegurar
        el rate configurado.
        Si el tiempo de procesamiento es superior a lo indicado por el rate se procesa si espera el mensaje.

        :param rate: Delay en milisegundos que se retrasará el procesamiento de los elementos del flujo
        :param must_apply: Si es verdadero se aplica el delay establecido
        """
        return FRateRPS(self, rate=rate, must_apply=must_apply)

    def chunks(self, n):
        """
        Emite un valor construido como una lista de como máximo n valores obtenidos del flujo padre.
        Si algún valor mientras se construye el chunk da error se emiten los elementos recolectados
        y luego se propaga el error.

        :param n: Cantidad de elementos recolectados antes de emitir el evento de lista.
        """
        return FChunks(n, self)

    def take(self, n, predicate=None):
        """
        Corta la ejecución del flujo luego de n elementos procesados.

        :param n: Cantidad de elementos procesados antes de cortar el flujo
        :param predicate: función(value, context) Si esta función retorna verdadero ese elemento es tomado en cuenta
        """
        return FTake(n, predicate, self)

    def take_until_seconds(self, n):
        """
        Corta la ejecución del flujo luego de n segundos de procesamiento.
        La ejecición se cortará si al momento de evaluar este paso el tiempo transcurrido fue superior
        al configurado.

        :param n: Cantidad de segundos que el stream procesará elementos.
        """
        return FTakeDuringTimeDelta(n, self)

    def log(self, build_log_message=lambda v, c: str(v), build_error_message=lambda e, c: str(e), level=logging.INFO):
        """
        Recibe una función(valor, contexto) que retorna un mensaje de texto que será logueado con el
        nivel de log indicado en level.
        El logueo se hace de forma asincrónica y no afecta al flujo.

        :param build_log_message: Función que dado un valor y contexto retorna un mensaje a loguear
        :param build_error_message: Función que dada una excepción y el contexto retorna el mensaje a loguear como ERROR
        :param level: Nivel de logueo que se usará
        """
        def log_function(l, msg, v, c):
            message = msg(v, c)
            if l is logging.WARNING or l is logging.WARN:
                logging.warning(message)
            elif l is logging.INFO:
                logging.info(message)
            elif l is logging.DEBUG:
                logging.debug(message)

        def log_error(msg, e, c):
            message = msg(e, c)
            logging.error(message)

        return FDoOnNext(partial(log_function, level, build_log_message), partial(log_error, build_error_message), True, self)

    def parallel(self, pool_size=5, join_timeout=0.001, metric_function=None, metric_rate=10, metric_buffer_size=10):
        """
        Ejecuta la obtención de elementos del stream en paralelo

        :param pool_size: Pool de hilos a utilizar
        :param join_timeout: Tiempo de espera de join en segundos por cada hilo (decimal)
        :param metric_function: función(metrics, contexto) Esta es una función que si se setea recibe con cada elemento
        procesado un bloque de métricas sobre la ejecución paralela y el contexto del último elemento recibido
        :param metric_rate: Cantidad de evaluaciones por segundo que se ejecuta la función metric_function.
        Si es None se ejecuta siempre
        :param metric_buffer_size: Tamaño del buffer utilizado para generar las métricas recibidas por metric_function
        """
        return FParallel(pool_size, join_timeout, metric_function, metric_rate, metric_buffer_size, self)

    def on_error_resume(self, resume=fu.default_error_resume, exceptions=[Exception]):
        """
        En caso de error, este paso ejecuta la función resume que debe retornar un valor
        a partir del error recibido por parámetro.

        :param resume: función(ex, contexto) Debe retornar el valor a substituir en el flujo.
        :param exceptions: Lista de excepciones para los que se aplica el resume.
        """
        return FOnErrorResume(resume, exceptions, self)

    def on_error_retry(self, retries=3, delay_ms=lambda i: 0, exceptions=[Exception]):
        """
        En caso de error este paso reintenta ejecutar el flujo retries veces más. Esto
        lo hace sólo para las excepciones indicadas por exceptions y los reintentos
        tienen un delay dado por la función delay_ms que recibe el número de reintento que
        es y espera obtener los ms de delay que se deben aplicar.

        :param retries: Cantidad de reintentos a aplicar
        :param delay_ms: función(int) que retorna dado el número de reintento en el que se está cuantos
                  ms de delay se deben aplicar.
        :param exceptions: Lista de excepciones para los que se aplica el resume.
        """
        return FOnErrorRetry(retries, exceptions, delay_ms, self)

    def subscribe(self, context={}, skip_error=False):
        """
        Crea un objeto iterable a partir del flujo. Si se itera sobre este objeto se obtendrán
        los valores del flujo.
        :param skip_error: Ignora errores al obtener los valores desde el flujo
        :param context: Contexto inicial para el flujo
        :return: Objeto iterable
        """
        return SSubscribe(skip_error, context, self)

    def foreach(self, on_success=fu.default_success, on_error=fu.default_error, on_finish=fu.default_finish, context={}):
        """
        Itera sobre los elementos del flujo e invoca a funciones on_success y on_error dependiendo
        el estado del flujo.
        :param on_success: función(valor, contexto) se invoca si el flujo procesa correctamente un valor
        :param on_error:  función(ex, valor, contexto) se invoca si hay un error en el flujo.
                          Esto no corta el procesamiento a menos que se lance una excepción en el método
        :param on_finish: función(contexto) se invoca al finalizar el flujo
        :param context: Contexto inicial para el flujo
        """
        flux = self.subscribe(context, True)
        while True:
            try:
                value = next(flux)
                fu.try_or(partial(on_success), value, context)
            except StopIteration:
                fu.try_or(partial(on_finish), context)
                return
            except Exception as ex:
                _, e = fu.try_or(partial(on_error), ex, value, context)

    def to_list(self, context={}, skip_error=True):
        """
        Itera sobre los elementos del flujo y los retorna todos dentro de una lista.
        :param context: contexto inicial para el flujo
        :param skip_error: Ignora errores al obtener los valores desde el flujo
        :return: Lista de elementos
        """
        return list(iter(self.subscribe(context, skip_error)))

    def collect(self, init=lambda c: {}, reduce=lambda v, a: a, context={}):
        """
        Permite agrupar en un sólo objeto el resultado del procesamiento de todos los elementos del flujo.
        Se inicializa un acumulador a través de la función init(contexto) y luego para cada elemento del flujo
        se invoca la función reduce(valor, acumulador) que procesa el valor y retorna un nuevo valor del acumulador.
        :param init: función(contexto) Retorna valor inicial del acumulador
        :param reduce: funcón(valor, acumulador) Dados el nuevo valor y el acumulador retorna un nuevo valor de acumulador.
        :param context: Contexto inicial para el flujo
        :return: Acumulador
        """
        acum = init(context)
        flux = self.subscribe(context, False)
        while True:
            try:
                value = next(flux)
                acum = reduce(value, acum)
            except StopIteration:
                return
            except Exception as ex:
                raise ex


class Stream(Flux):
    def __init__(self, up):
        super(Stream, self).__init__()
        self.upstream = up

    def prepare_next(self):
        self.upstream.prepare_next()

    def next(self, context):
        value, e, ctx = self.upstream.next(context)
        return value, e, ctx


class FFilter(Stream):
    def __init__(self, p, m, flux):
        super().__init__(flux)
        self.predicate = p
        self.on_mismatch = m

    def next(self, context):
        value, e, ctx = super(FFilter, self).next(context)
        if e is not None:
            return value, e, ctx

        valid, e = fu.try_or(partial(self.predicate), value, ctx)
        while e is None and not valid:
            _, e = fu.try_or(partial(self.on_mismatch), value, ctx)
            if e is not None:
                return value, e, ctx
            super(FFilter, self).prepare_next()
            value, e, new_ctx = super(FFilter, self).next(ctx)
            if e is not None:
                return value, e, ctx
            ctx = merge(ctx, new_ctx)
            valid, e = fu.try_or(partial(self.predicate), value, ctx)
        return value, e, ctx


class FMapIf(Stream):
    def __init__(self, p, f, flux):
        super().__init__(flux)
        self.predicate = p
        self.function = f

    def next(self, context):
        value, e, ctx = super(FMapIf, self).next(context)
        if e is not None:
            return value, e, ctx

        valid, e = fu.try_or(partial(self.predicate), value, ctx)
        if e is not None:
            return value, e, ctx

        if valid:
            v, e = fu.try_or(partial(self.function), value, ctx)
            if e is not None:
                return value, e, ctx
            return v, e, ctx

        return value, e, ctx


class FTake(Stream):
    def __init__(self, count, predicate, flux):
        super().__init__(flux)
        self.count = count
        self.predicate = predicate
        self.idx = 0

    def next(self, context):
        value, e, ctx = super(FTake, self).next(context)
        if e is not None:
            return value, e, ctx
        if self.predicate is not None:
            valid, e = fu.try_or(partial(self.predicate), value, ctx)
            if e is not None:
                return value, e, ctx
        else:
            valid = True
        if valid:
            self.idx = self.idx + 1
        if self.idx <= self.count:
            return value, e, ctx
        else:
            return value, StopIteration(), ctx


class FTakeDuringTimeDelta(Stream):
    def __init__(self, td, flux):
        super().__init__(flux)
        if type(td) == timedelta:
            self.timedelta = td
        if type(td) == int or type(td) == float:
            self.timedelta = datetime.timedelta(seconds=td)
        self.starttime = None

    def next(self, context):
        if self.starttime is None:
            self.starttime = datetime.utcnow()

        value, e, ctx = super(FTakeDuringTimeDelta, self).next(context)
        if self.starttime + self.timedelta >= datetime.utcnow():
            return value, e, ctx
        else:
            return value, StopIteration(), ctx


class FChunks(Stream):
    def __init__(self, count, flux):
        super().__init__(flux)
        self.count = count
        self.buffer = []
        self.stop_iteration = False

    def prepare_next(self):
        if not self.stop_iteration:
            super(FChunks, self).prepare_next()

    def next(self, context):
        if self.stop_iteration:
            return self.buffer, StopIteration(), context
        ctx = context
        while len(self.buffer) < self.count:
            value, e, new_ctx = super(FChunks, self).next(ctx)
            if e is not None:
                self.stop_iteration = True
                if len(self.buffer) == 0:
                    return self.buffer, StopIteration(), ctx
                buf = self.buffer.copy()
                self.buffer = []
                return buf, None, ctx
            self.buffer.append(value)
            super(FChunks, self).prepare_next()
            ctx = merge(ctx, new_ctx)
        buf = self.buffer.copy()
        self.buffer = []
        return buf, None, ctx


class FDelayMs(Stream):
    def __init__(self, delay, predicate, flux):
        super().__init__(flux)
        self.delay = delay
        self.predicate = predicate

    def next(self, context):
        value, e, ctx = super(FDelayMs, self).next(context)
        if e is not None:
            return value, e, ctx
        valid, e = fu.try_or(partial(self.predicate), value, ctx)
        if e is not None:
            return value, e, ctx
        if valid:
            time.sleep(self.delay / 1000)
        return value, e, ctx


class FRateRPS(Stream):
    def __init__(self, rate, must_apply, flux):
        super().__init__(flux)
        self.rate = rate
        self.predicate = must_apply

    def next(self, context):
        start_time = time.monotonic()
        value, e, ctx = super(FRateRPS, self).next(context)
        if e is not None:
            return value, e, ctx
        end_time = time.monotonic()

        valid, e = fu.try_or(partial(self.predicate), value, ctx)
        if e is not None:
            return value, e, ctx
        if valid:
            delay = (1 / self.rate) - (end_time - start_time)
            if delay > 0:
                time.sleep(delay)
        return value, e, ctx


class _Register:

    def __init__(self):
        self.value = None
        self.e = None
        self.ctx = None
        self.elapsed_time = 0

    def execute(self, sup, context):
        t = time.monotonic()
        sup.prepare_next()
        self.value, self.e, ctx = sup.next(context)
        self.ctx = merge(context, ctx)
        self.elapsed_time = (time.monotonic() - t)
        return self


class FParallel(Stream):
    def __init__(self, pool_size, join_timeout, metric_func, metric_rate, metric_buffer_size, flux):
        super().__init__(flux)
        self.pool_size = pool_size
        self.join_timeout = join_timeout
        self.metric_func = metric_func
        self.metric_rate = metric_rate
        self.metric_buffer_size = metric_buffer_size
        self.executor = cr.ThreadPoolExecutor(max_workers=pool_size)
        self.semaphore = threading.BoundedSemaphore(pool_size)
        self.futures = []
        self.buffer_metrics = []
        self.last_metric_execution = time.monotonic()
        self.waiting_to_stop = False

    def show_metrics(self, elapsed_time, ctx):
        if self.metric_func is not None:
            now = time.monotonic()
            self.buffer_metrics.append((len(self.futures), elapsed_time, now))
            len_buffer = len(self.buffer_metrics)
            if len_buffer >= self.metric_buffer_size:
                self.buffer_metrics.pop(0)

            if len_buffer > 0:
                diff_time = max(map(lambda p: p[2], self.buffer_metrics)) - min(map(lambda p: p[2], self.buffer_metrics))
                metrics = {
                    'pool_size': self.pool_size,
                    'used_pool': len(self.futures),
                    'avg_used_pool': round(mean(map(lambda p: p[0], self.buffer_metrics)), 2),
                    'avg_task_time_ms': round(mean(map(lambda p: p[1], self.buffer_metrics)) * 1000, 2),
                    'rate_rps': round(len(self.buffer_metrics) / diff_time if diff_time > 0 else 0.0, 2)
                }
                if self.metric_rate is None or (now - self.last_metric_execution) > (1 / self.metric_rate):
                    self.metric_func(metrics, ctx)
                    self.last_metric_execution = now
        self.last_metric_execution = now

    def next(self, context):
        while not self.waiting_to_stop or len(self.futures) > 0:
            if not self.waiting_to_stop:
                self.semaphore.acquire()
                try:
                    future = self.executor.submit(_Register().execute, super(FParallel, self), context)
                    self.futures.append(future)
                except:
                    self.semaphore.release()
                    raise
                else:
                    future.add_done_callback(lambda x: self.semaphore.release())
            try:
                futures = self.futures.copy()
                for future in cr.as_completed(futures, timeout=self.join_timeout):
                    self.futures.remove(future)
                    r = future.result()
                    self.show_metrics(r.elapsed_time, r.ctx)
                    if not self.waiting_to_stop and r.e is not None and isinstance(r.e, StopIteration):
                        self.waiting_to_stop = True
                        self.executor.shutdown(wait=True)
                        break
                    if r.e is None or not isinstance(r.e, StopIteration):
                        return r.value, r.e, r.ctx
            except TimeoutError:
                pass
        return None, StopIteration(), {}


class FMap(Stream):
    def __init__(self, func, flux):
        super().__init__(flux)
        self.function = func

    def next(self, context):
        value, e, ctx = super(FMap, self).next(context)
        if e is not None:
            return value, e, ctx
        mapped_value, e = fu.try_or(partial(self.function), value, ctx.copy())
        if e is not None:
            return value, e, ctx
        return mapped_value, e, ctx


class FMapContext(Stream):
    def __init__(self, func, flux):
        super().__init__(flux)
        self.function = func

    def next(self, context):
        value, e, ctx = super(FMapContext, self).next(context)
        if e is not None:
            return value, e, ctx
        mapped_context, e = fu.try_or(partial(self.function), value, ctx.copy())
        if e is not None:
            return value, e, ctx
        return value, e, merge(ctx, mapped_context)


class FFlatMap(Stream):
    def __init__(self, func, flux):
        super().__init__(flux)
        self.function = func
        self.current = None

    def prepare_next(self):
        if self.current is None:
            super(FFlatMap, self).prepare_next()
        else:
            self.current.prepare_next()

    def next(self, context):
        ctx = context.copy()
        while True:
            while self.current is None:
                value, e, ctx = super(FFlatMap, self).next(ctx)
                if e is not None:
                    return None, e, ctx
                func, e = fu.try_or(partial(self.function), value, ctx)
                if e is not None:
                    return None, e, ctx
                fgen = func
                if isinstance(func, types.GeneratorType):
                    from python_flux.producers import PFromGenerator
                    fgen = PFromGenerator(func)
                self.current = fgen
                self.current.prepare_next()

            cur_value, cur_e, cur_ctx = self.current.next(ctx)
            if cur_e is None:
                return cur_value, cur_e, cur_ctx
            if isinstance(cur_e, StopIteration):
                self.current = None
                super(FFlatMap, self).prepare_next()
            ctx = merge(ctx, cur_ctx)


class FOnErrorResume(Stream):
    def __init__(self, f, exceptions, flux):
        super().__init__(flux)
        self.on_error_resume = f
        self.exceptions = exceptions

    def next(self, context):
        value, e, ctx = super(FOnErrorResume, self).next(context)
        if e is None:
            return value, e, ctx
        if isinstance(e, StopIteration):
            return None, e, ctx
        if any([isinstance(e, ex) for ex in self.exceptions]):
            v, e = fu.try_or(partial(self.on_error_resume), e, value, ctx)
            if e is not None:
                return value, e, ctx
            value = v
        return value, None, ctx


class FOnErrorRetry(Stream):
    def __init__(self, retries, exceptions, delay_ms, flux):
        super().__init__(flux)
        self.retries = retries
        self.exceptions = exceptions
        self.delay_ms = delay_ms
        self.current_retries = retries

    def prepare_next(self):
        super(FOnErrorRetry, self).prepare_next()
        self.current_retries = self.retries

    def next(self, context):
        value, e, ctx = super(FOnErrorRetry, self).next(context)
        while e is not None and self.current_retries > 0:
            d = self.delay_ms(self.retries - self.current_retries) / 1000
            if d > 0:
                time.sleep(d)
            self.current_retries = self.current_retries - 1
            value, e, ctx = super(FOnErrorRetry, self).next(context)
        return value, e, ctx


class FDoOnNext(Stream):

    def __init__(self, on_next, on_error, exec_async, flux):
        super().__init__(flux)
        self.on_next = on_next
        self.on_error = on_error
        self.execute_async = exec_async

    def next(self, context):
        value, e, ctx = super(FDoOnNext, self).next(context)
        if e is not None:
            if self.execute_async:
                t = threading.Thread(target=self.on_error, args=(e, ctx,))
                t.start()
            else:
                self.on_error(e, ctx)
            return value, e, ctx
        if self.execute_async:
            t = threading.Thread(target=self.on_next, args=(value, ctx,))
            t.start()
        else:
            self.on_next(value, ctx)
        return value, e, ctx
