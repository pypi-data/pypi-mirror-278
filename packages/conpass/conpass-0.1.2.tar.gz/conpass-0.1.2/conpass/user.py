from enum import Enum
from datetime import datetime, timedelta, timezone


class USER_STATUS(Enum):
    FOUND = 0
    THRESHOLD = 1
    PSO = 2
    UNREADABLE_PSO = 3
    TESTED = 4
    TEST = 5


class User:
    def __init__(self, samaccountname, dn, last_password_test, bad_password_count, lockout_reset, lockout_threshold, pso, time_delta, console, debug):
        self.samaccountname = samaccountname
        self.dn = dn
        self.password = None
        self.last_password_test = last_password_test
        self.bad_password_count = bad_password_count
        self.lockout_reset = -(lockout_reset/10000000/60)
        self.lockout_threshold = lockout_threshold
        self.pso = pso
        self.first_attempt = True
        self.time_delta = time_delta
        self.console = console
        self.debug = debug

        if self.pso is not None and self.pso.readable:
            self.lockout_threshold, self.lockout_reset = self.pso.lockout_threshold, -(self.pso.lockout_window/10000000/60)


        self.debug and self.console.log(f"{self.samaccountname}\tLast pwd test : {self.last_password_test} - Lockout threshold {self.bad_password_count}/{self.lockout_threshold} - Reset {self.lockout_reset} min")
        self.debug and self.console.log(f"\tWhen it can be changed: {self.last_password_test + timedelta(minutes=self.lockout_reset)}")
        self.debug and self.console.log(f"\tServer time:            {datetime.now(timezone.utc) - self.time_delta}")

    def check_lockout(self, security_threshold):
        # Skip users with bad password count close to lockout threshold and still in of observation window
        return self.lockout_threshold > 0 and (
                self.lockout_threshold <= security_threshold or
                (
                        self.bad_password_count >= (self.lockout_threshold - security_threshold)
                        and (self.last_password_test + timedelta(minutes=self.lockout_reset) + timedelta(seconds=5) > datetime.now(timezone.utc) - self.time_delta)
                )
        )
    def should_test_password(self, security_threshold=1, ldapconnection=None):
        # Checking all PSO applied to user. If one PSO is not readable (access denied), the user should not be tested
        # as the PSO might be more strict than the global password policy

        if self.readable_pso() == -1:
            return USER_STATUS.UNREADABLE_PSO

        if self.pso is not None:
            self.lockout_threshold, self.lockout_reset = self.pso.lockout_threshold, -(self.pso.lockout_window/10000000/60)

        # Skip users if password already found
        if self.password is not None:
            return USER_STATUS.FOUND

        # Skip users with bad password count close to lockout threshold and still in of observation window
        if self.check_lockout(security_threshold):
            return USER_STATUS.THRESHOLD

        # Update user with latest infos in case a real user has entered a bad password
        # This is only necessary when lockout threshold is > 0 and it is considered to be valid for testing in this tool
        self.lockout_threshold > 0 and self.update(*ldapconnection.get_user(self.samaccountname))

        # Now, with updated information, check again for lockout risk
        if self.check_lockout(security_threshold):
            return USER_STATUS.THRESHOLD

        if self.lockout_threshold > 0 and self.last_password_test + timedelta(minutes=self.lockout_reset) + timedelta(seconds=1) <= datetime.now(timezone.utc) - self.time_delta:
            # Bad password count is reset to 0
            self.debug and self.console.log(f"{self.samaccountname} - Reset {self.lockout_reset} min has passed, bad_password_count reset")
            self.bad_password_count = 0

        if self.lockout_threshold > 0 or self.bad_password_count < (self.lockout_threshold - security_threshold):
            self.debug and self.console.log(f"{self.samaccountname} - {self.bad_password_count}/{self.lockout_threshold}")
        else:
            self.debug and self.console.log(f"{self.samaccountname} - {self.bad_password_count}/{self.lockout_threshold}")
            self.debug and self.console.log(f"{self.last_password_test + timedelta(minutes=self.lockout_reset)} is less than...")
            self.debug and self.console.log(f"{datetime.now(timezone.utc) - self.time_delta} ?")

        self.first_attempt = False

        if self.readable_pso() == 1:
            return USER_STATUS.PSO
        return USER_STATUS.TEST

    def update(self, last_password_test, bad_password_count):

        if bad_password_count != self.bad_password_count:
            update_text = f"{self.samaccountname} 'badPwdCount' changed from {self.bad_password_count} to {bad_password_count}"
            self.console.log()
            if self.last_password_test > last_password_test:
                self.console.log(f"{update_text} - You may have tried the N-1 or N-2 user's password!")
            else:
                if self.bad_password_count > bad_password_count:
                    self.console.log(f"{update_text} - The user may have logged in")
                else:
                    self.console.log(f"{update_text} - The user may have entered a bad password")
            self.console.log(f"{self.last_password_test} to {last_password_test}")
            self.bad_password_count = bad_password_count

        self.last_password_test = last_password_test

    def should_be_discarded(self):
        # Password already found
        if self.password is not None:
            return USER_STATUS.FOUND

        # Cannot read PSO, so should be discarded
        if self.readable_pso() == -1:
            return USER_STATUS.UNREADABLE_PSO

        # Has PSO, but can be read, should be tested
        if self.readable_pso() == 1:
            return USER_STATUS.PSO

        # Default domain policy, should be tested
        return USER_STATUS.TEST

    def readable_pso(self):
        if self.pso is None:
            return 0
        return 1 if self.pso.readable else -1

    def test_password(self, password, conn, thread_name=""):
        self.last_password_test = datetime.now(timezone.utc) - self.time_delta
        if not conn.test_credentials(self.samaccountname, password):
            self.bad_password_count += 1
            return False
        self.password = password
        return True

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.samaccountname == other.samaccountname

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User(samAccountName={self.samaccountname}, password={self.password}, last_password_test={self.last_password_test}, bad_password_count={self.bad_password_count}, lockout_reset={self.lockout_reset}, lockout_threshold={self.lockout_threshold}, pso={self.pso})"
