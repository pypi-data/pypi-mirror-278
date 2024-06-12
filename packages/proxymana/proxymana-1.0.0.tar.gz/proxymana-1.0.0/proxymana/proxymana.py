import threading
import time
import lxml.html as lh

import requests
import schedule


SSL_PROXIES_URL = "https://www.sslproxies.org/"
GOOGLE_URL = "https://www.google.com/"


class ProxyMana:

    available_proxies = list()
    invalid_proxies = list()
    proxy_timeout = None
    proxy_search_freq = None
    proxy_clear_freq = None
    verbose = False
    _available_proxies_busy = False
    _invlaid_proxies_busy = False
    _keep_running_scheduler = False
    _scheduler_running = False
    _thread_lock = threading.Lock()

    def __init__(self):
        """
        ProxyMana is a proxy manager that periodically searches and manages new free proxies from <https://www.sslproxies.org/>.

        Available methods:
            start_scheduler_thread: Starts a scheduler thread to periodically update the available proxies and clear invalid proxies.
            stop_scheduler_thread: Stops the scheduler thread.
            get_new_proxy: Gets a new proxy from the available proxies list.
            remove_proxy: Removes a proxy from the invalid proxies list.
        """

    @classmethod
    def start_scheduler_thread(
        cls, proxy_timeout=1, proxy_search_freq=1, proxy_clear_freq=120, verbose=False
    ):
        """
        Starts a scheduler thread to periodically update the available proxies and clear invalid proxies.

        Args:
            proxy_timeout (int, optional): The timeout value for the proxies. Defaults to 1.
            proxy_search_freq (int, optional): The frequency (in seconds) at which to search for new proxies. Defaults to 1.
            proxy_clear_freq (int, optional): The frequency (in seconds) at which to clear invalid proxies. Defaults to 120.
            verbose (bool, optional): Whether to print verbose output. Defaults to False.

        Returns:
            None
        """

        # lock the thread to ensure only one scheduler thread is running
        with cls._thread_lock:
            # if the scheduler is not already started
            if not cls._scheduler_running:

                # update the class attributes
                cls._keep_running_scheduler = True
                cls.verbose = verbose
                cls.proxy_timeout = proxy_timeout
                cls.proxy_search_freq = proxy_search_freq
                cls.proxy_clear_freq = proxy_clear_freq

                # start the scheduler thread
                scheduler_thread = threading.Thread(target=cls._start_scheduler)
                scheduler_thread.daemon = True
                scheduler_thread.start()

    @classmethod
    def stop_scheduler_thread(cls):
        """
        Stops the scheduler thread.

        Args:
            None

        Returns:
            None
        """

        cls._keep_running_scheduler = False

        if cls.verbose:
            while True:
                if not cls._scheduler_running:
                    print("Scheduler stopped.")
                    break

                time.sleep(0.5)

    @classmethod
    def get_new_proxy(cls):
        """
        Get a new proxy from the available proxies list.

        Args:
            None

        Returns:
            str: The new proxy.

        """

        # try until the proxies lists are accessible
        while cls._keep_running_scheduler:
            if not cls._available_proxies_busy and not cls._invlaid_proxies_busy:

                cls._available_proxies_busy = True
                cls._invlaid_proxies_busy = True

                # iterate over the available proxies and return the first valid one
                for proxy in cls.available_proxies:
                    if proxy not in cls.invalid_proxies:

                        cls._available_proxies_busy = False
                        cls._invlaid_proxies_busy = False
                        return proxy

                cls._available_proxies_busy = False
                cls._invlaid_proxies_busy = False

            time.sleep(0.5)

        # if the scheduler is not running
        return None

    @classmethod
    def remove_proxy(cls, proxy):
        """
        Adds a proxy to the list of invalid proxies.

        Args:
            proxy (str): The proxy to be added to the list of invalid proxies.

        Returns:
            None
        """

        # try until the invalid proxies list is accessible
        while True:
            if not cls._invlaid_proxies_busy:
                cls._invlaid_proxies_busy = True
                cls.invalid_proxies.append(proxy)
                cls._invlaid_proxies_busy = False

                break

            time.sleep(0.1)

    @classmethod
    def _start_scheduler(cls):
        """
        Starts the scheduler to periodically update the available proxies and clear invalid proxies.

        Args:
            None

        Returns:
            None
        """

        # configure the scheduler
        schedule.every(cls.proxy_search_freq).seconds.do(cls._update_available_proxies)
        schedule.every(cls.proxy_clear_freq).seconds.do(cls._clear_invalid_proxies)

        # run the scheduler for the first time
        schedule.run_all()

        cls._scheduler_running = True

        # run the scheduler in an infinite loop
        while cls._keep_running_scheduler:
            schedule.run_pending()
            time.sleep(0.5)

        cls._scheduler_running = False

    @classmethod
    def _update_available_proxies(cls):
        """
        Updates the list of available proxies by scraping the SSLProxies website.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: If there is an error retrieving the proxies or checking their status.
        """

        new_proxies = list()

        try:
            # get the proxies from the SSLProxies website
            response = requests.get(SSL_PROXIES_URL)
            doc = lh.fromstring(response.content)
            tr_elements = doc.xpath('//*[@id="list"]//tr')

            # iterate over the proxies and check their status
            for i in range(1, len(tr_elements)):
                ip_address = tr_elements[i][0].text_content()
                port = tr_elements[i][1].text_content()
                proxy = f"http://{ip_address}:{port}"

                # if the proxy is valid
                if cls._keep_running_scheduler and cls._check_proxy_status(proxy):

                    # add the proxy to the list of new proxies
                    new_proxies.append(proxy)

                    # as soon as a valid proxy is found, add it to the list of available proxies
                    while True:
                        if not cls._available_proxies_busy:
                            cls._available_proxies_busy = True
                            if proxy not in cls.available_proxies:
                                cls.available_proxies.append(proxy)
                            cls._available_proxies_busy = False
                            break

                        time.sleep(0.1)

        except Exception:
            pass

        # update the list of available proxies with the new ones
        while True:
            if not cls._available_proxies_busy:
                cls._available_proxies_busy = True
                if new_proxies:
                    cls.available_proxies = new_proxies
                    if cls.verbose:
                        print("Available proxies updated.")
                        print(
                            f"- Current available proxies: {len(cls.available_proxies)}."
                        )
                        print(f"- Current invalid proxies: {len(cls.invalid_proxies)}.")

                cls._available_proxies_busy = False
                break

            time.sleep(0.1)

    @classmethod
    def _clear_invalid_proxies(cls):
        """
        Clears the list of invalid proxies.

        Args:
            None

        Returns:
            None
        """

        # try until the invalid proxies list is accessible
        while True:
            if not cls._invlaid_proxies_busy:
                cls._invlaid_proxies_busy = True
                cls.invalid_proxies = list()
                if cls.verbose:
                    print("Invalid proxies cleared.")
                cls._invlaid_proxies_busy = False
                break
            time.sleep(0.1)

    @classmethod
    def _check_proxy_status(cls, proxy):
        """
        Checks the status of a proxy by making a request to a test URL.

        Args:
            proxy (str): The proxy to check.

        Returns:
            bool: True if the proxy is valid, False otherwise.

        Raises:
            Exception: If there is an error making the request.
        """

        try:
            # make a request to a test URL using the proxy
            with requests.get(
                GOOGLE_URL,
                proxies={"https": proxy},
                timeout=cls.proxy_timeout,
                stream=True,
            ) as response:
                # if the proxy is valid, return True
                if (
                    response.raw.connection.sock
                    and response.raw.connection.sock.getpeername()[0]
                    == proxy.split(":")[1][2:]
                ):
                    return True

        # if the proxy is invalid, return False
        except Exception:
            return False
