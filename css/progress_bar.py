def build_timer(time):
    timer_html = """
<script>
function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        hours = parseInt(timer / 3600, 10);
        minutes = parseInt((timer % 3600) / 60, 10);
        seconds = parseInt(timer % 60, 10);

        hours = hours < 10 ? "0" + hours : hours;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = hours + ":" + minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}

window.onload = function () {
    display = document.querySelector('#time');
    startTimer("""+(str(time.total_seconds()))+""", display);
};
</script>

<style>
      progress[value] {
        appearance: none;
        width: 100%;
        height: 15px;
      }

      progress::-webkit-progress-bar {
        background-color: #F1F1F1;
        border-radius: 10em;
      }
      progress::-webkit-progress-value {
        border-radius: 10em;
        background-color: #0F596E;
      }
    </style>

<html>
  <center>
  <h4 style='font-family: "Source Sans Pro", sans-serif; font-weight: 600; color: rgb(49, 51, 63); line-height: 1.2; margin-bottom: 0px; margin-top: 0px;'>Poll will close in <span id="time">...</span></h4>
  </center>
  <progress id="file" max="100" value=\""""+(str(100-((time.total_seconds() / 14400) * 100)))+"""\"/progress>
  </html>
"""
    return timer_html