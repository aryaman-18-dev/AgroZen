from pathlib import Path
p=Path('auth.js'); s=p.read_text(encoding='utf-8')
old='''  async logout() {
    try {
      const { auth } = await getFirebaseInstances();
      await signOut(auth);
      sessionStorage.removeItem("AgroZen_session");
      this.currentUser = null;
      window.location.href = "login.html";
      return { success: true };
    } catch (err) {
      return { success: false, message: err.message };
    }
  }'''
new='''  async logout({ redirect = true } = {}) {
    let logoutError = null;
    try {
      const { auth } = await getFirebaseInstances();
      await signOut(auth);
    } catch (err) {
      logoutError = err;
    } finally {
      sessionStorage.removeItem("AgroZen_session");
      this.currentUser = null;
      this._ready = true;
    }

    if (redirect) window.location.replace("login.html");
    return logoutError
      ? { success: false, message: logoutError.message }
      : { success: true, message: "You have been logged out." };
  }'''
if old not in s: raise SystemExit('logout implementation not found')
p.write_text(s.replace(old,new),encoding='utf-8')
p=Path('main.html'); s=p.read_text(encoding='utf-8')
s=s.replace('<script src="auth.js"></script>','<script type="module" src="auth.js"></script>',1)
old='''    function showLogoutConfirmation() {
      Swal.fire({'''
new='''    async function showLogoutConfirmation() {
      const confirmation = await Swal.fire({'''
if old not in s: raise SystemExit('confirmation function not found')
s=s.replace(old,new,1)
old='''      }).then((result) => {
        if (result.isConfirmed) {
          const logoutResult = window.authManager.logout();
          if (logoutResult.success) {
            Swal.fire({
              title: 'Logged Out!',
              text: logoutResult.message,
              icon: 'success',
              timer: 2000,
              showConfirmButton: false
            }).then(() => {
              window.location.href = 'index.html';
            });
          } else {
            Swal.fire({
              title: 'Error!',
              text: logoutResult.message,
              icon: 'error'
            });
          }
        }
      });
    }'''
new='''      });
      if (!confirmation.isConfirmed) return;

      const logoutResult = await window.authManager.logout({ redirect: false });
      if (logoutResult.success) {
        await Swal.fire({
          title: 'Logged Out!',
          text: logoutResult.message,
          icon: 'success',
          timer: 1200,
          showConfirmButton: false
        });
        window.location.replace('index.html');
      } else {
        await Swal.fire({
          title: 'Local session cleared',
          text: `Firebase sign-out reported an error: ${logoutResult.message}`,
          icon: 'warning'
        });
        window.location.replace('login.html');
      }
    }'''
if old not in s: raise SystemExit('confirmation result block not found')
p.write_text(s.replace(old,new,1),encoding='utf-8')
