class Chatbox {
  constructor() {
    this.args = {
      chatSection : document.querySelector(".chatbox"),
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };
    
    this.state = false;
    this.message = [{ name: "Sam", message: "Hello, I'm AI Version of Sujal (Currently in Beta)! Ask me anything!"}];
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;
    openButton.addEventListener("click", () => this.toggleState(chatBox));
    sendButton.addEventListener("click", () => this.onSendMessage(chatBox));

    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", (key) => {
      if (key.keyCode === 13) {
        this.onSendMessage(chatBox);
      }
    });
  }

  toggleState(chatBox) {
    this.state = !this.state;

    if (this.state) {
      // change the z-index of chatSection
      this.args.chatSection.style.zIndex = 1000;
      chatBox.classList.add("chatbox--active");
    } else {
      // change the z-index of chatSection
      this.args.chatSection.style.zIndex = -123456;
      chatBox.classList.remove("chatbox--active");
    }
  }

  onSendMessage(chatBox) {
    var textField = chatBox.querySelector("input");
    var text1 = textField.value;
    if (text1 === "") {
      return;
    }
    setTimeout(() => {
      textField.value = "";
      this.message.push({ name: "Sam", message: "I'm typing..." });
      this.updateChatText(chatBox);
    }, 1000);

    let msg = { name: "User", message: text1 };
    this.message.push(msg);
    fetch($SCRIPT_ROOT + "/predict", {
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(r => r.json())
      .then(r => {
        this.message.pop();
        let msg2 = { name: "Sam", message: r.answer};
        this.message.push(msg2);
        
        this.updateChatText(chatBox);
        textField.value = "";

      })
      .catch((error) => {
        console.error("Error:", error);
        this.updateChatText(chatBox);
        textField.value = "";
      });
  }

  updateChatText(chatBox) {
    var html = "";
    this.message
      .slice()
      .reverse()
      .forEach(function (item) {
        console.log(item);
        if (item.name === "Sam") {
          html +=
            '<div style="display: flex; align-items: end; gap:0.5rem;"><img style="width: 40px; height: 40px; border-radius: 50%;" src="../static/images/Demo.png" alt="image"> <div class="messages__item messages__item--visitor">' +
            item.message +
            "</div></div>";
        } else {
          html +=
            '<div class="messages__item messages__item--operator">' +
            item.message +
            "</div>";
        }
      });
    const chatmessage = chatBox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
  }
}

const chatbox = new Chatbox();
chatbox.display();
chatbox.updateChatText(document.querySelector(".chatbox__support"));
