/*
 * Sound Quiz Application
 *
 * This JavaScript file powers a simple multiple‑choice listening quiz.
 * Each question presents a sentence that is spoken aloud using the
 * browser's SpeechSynthesis API. Learners choose between two words
 * that sound similar. Correct selections trigger a friendly message
 * while incorrect choices prompt a gentle reminder.
 */

(() => {
  // Data set for the quiz.  Each object holds a sentence, two word
  // options, and the index of the correct option (0 or 1).  The
  // sentences are drawn from common homophones and near‑homophones.
  const quizData = [
    {sentence: 'I won\'t send a book.', options: ['won\'t', 'want'], correctIndex: 0},
    {sentence: 'He is here.', options: ['is', 'isn\'t'], correctIndex: 0},
    {sentence: 'We are late.', options: ['are', 'aren\'t'], correctIndex: 0},
    {sentence: 'You can make it.', options: ['can', 'can\'t'], correctIndex: 0},
    {sentence: 'We\'re going to win.', options: ['We\'re', 'Were'], correctIndex: 0},
    {sentence: 'We are lost.', options: ['are', 'aren\'t'], correctIndex: 0},
    {sentence: 'It is too late.', options: ['too', 'to'], correctIndex: 0},
    {sentence: 'They\'re my friends.', options: ['They\'re', 'Their'], correctIndex: 0},
    {sentence: 'You\'re absolutely right.', options: ['You\'re', 'Your'], correctIndex: 0},
    {sentence: 'He is taller than me.', options: ['than', 'then'], correctIndex: 0},
    {sentence: 'I always lose my socks.', options: ['lose', 'loose'], correctIndex: 0},
    {sentence: 'I can\'t decide whether to go.', options: ['whether', 'weather'], correctIndex: 0},
    {sentence: 'I can hear the music.', options: ['hear', 'here'], correctIndex: 0},
    {sentence: 'Our principal is very strict.', options: ['principal', 'principle'], correctIndex: 0},
    {sentence: 'I accept your offer.', options: ['accept', 'except'], correctIndex: 0},
    {sentence: 'This change will affect our plans.', options: ['affect', 'effect'], correctIndex: 0},
    {sentence: 'Please advise me on this.', options: ['advise', 'advice'], correctIndex: 0},
    {sentence: 'I want some dessert.', options: ['dessert', 'desert'], correctIndex: 0},
    {sentence: 'We visited the site of the battle.', options: ['site', 'sight'], correctIndex: 0},
    {sentence: 'Who\'s coming to the party?', options: ['Who\'s', 'Whose'], correctIndex: 0},
    {sentence: 'The car needs new brakes.', options: ['brakes', 'breaks'], correctIndex: 0},
    {sentence: 'Where did he go?', options: ['Where', 'Wear'], correctIndex: 0},
    {sentence: 'Give me a piece of cake.', options: ['piece', 'peace'], correctIndex: 0},
    {sentence: 'Please write your name here.', options: ['write', 'right'], correctIndex: 0},
    {sentence: 'I knew you would come.', options: ['knew', 'new'], correctIndex: 0},
    {sentence: 'Take a deep breath.', options: ['breath', 'breathe'], correctIndex: 0},
    {sentence: 'I hate math.', options: ['math', 'Mass'], correctIndex: 0},
    {sentence: 'The hike was hard, but it was worth it.', options: ['worth', 'worse'], correctIndex: 0},
    {sentence: 'He has three dogs.', options: ['three', 'tree'], correctIndex: 0},
    {sentence: 'I think so.', options: ['think', 'sink'], correctIndex: 0},
    {sentence: 'The cat has a small mouth.', options: ['mouth', 'mouse'], correctIndex: 0},
    {sentence: 'The path is clear.', options: ['path', 'pass'], correctIndex: 0},
    {sentence: 'Look at that ship.', options: ['ship', 'sheep'], correctIndex: 0},
    {sentence: 'She wants to live here.', options: ['live', 'leave'], correctIndex: 0},
    {sentence: 'He stepped on the glass.', options: ['glass', 'grass'], correctIndex: 0},
    {sentence: 'The kids love to play outside.', options: ['play', 'pray'], correctIndex: 0},
    {sentence: 'He tried to collect the papers.', options: ['collect', 'correct'], correctIndex: 0},
    {sentence: 'That doesn\'t feel light.', options: ['light', 'right'], correctIndex: 0},
    {sentence: 'We saw the van coming.', options: ['van', 'ban'], correctIndex: 0},
    {sentence: 'Look at the cloud.', options: ['cloud', 'crowd'], correctIndex: 0},
    {sentence: 'The plant glows at night.', options: ['glows', 'grows'], correctIndex: 0},
    {sentence: 'Use the lock to keep the door closed.', options: ['lock', 'rock'], correctIndex: 0},
    {sentence: 'He lost his cap.', options: ['cap', 'cup'], correctIndex: 0},
    {sentence: 'The baby sleeps in a cot.', options: ['cot', 'coat'], correctIndex: 0},
    {sentence: 'He packed the car.', options: ['packed', 'parked'], correctIndex: 0},
    {sentence: 'He has a fan in his room.', options: ['fan', 'van'], correctIndex: 0},
    {sentence: 'He beat her on stage in the play.', options: ['beat', 'bit'], correctIndex: 0},
    {sentence: 'He felt full after dinner.', options: ['full', 'fool'], correctIndex: 0},
    {sentence: 'Let\'s pool our money for the gift.', options: ['pool', 'pull'], correctIndex: 0},
    {sentence: 'I\'m going to bet on that horse.', options: ['bet', 'vet'], correctIndex: 0},
    {sentence: 'He took a bow after his performance.', options: ['bow', 'vow'], correctIndex: 0},
    {sentence: 'He broke the vase.', options: ['vase', 'base'], correctIndex: 0},
    {sentence: 'The car needs new brakes.', options: ['brakes', 'breaks'], correctIndex: 0},
    {sentence: 'He dropped the ball.', options: ['ball', 'bowl'], correctIndex: 0},
    {sentence: 'He blew out the candle.', options: ['blew', 'blue'], correctIndex: 0},
    {sentence: 'He threw the ball.', options: ['threw', 'through'], correctIndex: 0},
    {sentence: 'He led the team to victory.', options: ['led', 'lead'], correctIndex: 0},
    {sentence: 'Take off your shoes.', options: ['off', 'of'], correctIndex: 0},
    {sentence: 'He read the poem aloud.', options: ['aloud', 'allowed'], correctIndex: 0},
    {sentence: 'I have two cats.', options: ['two', 'to'], correctIndex: 0},
    {sentence: 'This costs four dollars.', options: ['four', 'for'], correctIndex: 0},
    {sentence: 'The wine complements the meal.', options: ['complements', 'compliments'], correctIndex: 0},
    {sentence: 'His patience was tested.', options: ['patience', 'patients'], correctIndex: 0},
    {sentence: 'The company has good personnel.', options: ['personnel', 'personal'], correctIndex: 0},
    {sentence: 'She is quite right.', options: ['quite', 'quiet'], correctIndex: 0},
    {sentence: 'This sand is coarse.', options: ['coarse', 'course'], correctIndex: 0},
    {sentence: 'It\'s an everyday occurrence.', options: ['everyday', 'every day'], correctIndex: 0},
    {sentence: 'He fought with his bare hands.', options: ['bare', 'bear'], correctIndex: 0},
    {sentence: 'He found a cache of jewels.', options: ['cache', 'cash'], correctIndex: 0},
    {sentence: 'He fired the cannon.', options: ['cannon', 'canon'], correctIndex: 0},
    {sentence: 'He chose the red one.', options: ['chose', 'choose'], correctIndex: 0},
    {sentence: 'Of the two choices, he preferred the latter.', options: ['latter', 'later'], correctIndex: 0},
    {sentence: 'My bike is stationary.', options: ['stationary', 'stationery'], correctIndex: 0},
    {sentence: 'The sky was lit up by lightning.', options: ['lightning', 'lightening'], correctIndex: 0},
    {sentence: 'He pedals his bike to work.', options: ['pedals', 'peddles'], correctIndex: 0},
    {sentence: 'She peeked at the present.', options: ['peeked', 'peaked'], correctIndex: 0},
    {sentence: 'She pored over the documents.', options: ['pored', 'poured'], correctIndex: 0},
    {sentence: 'There is a problem.', options: ['There', 'Their'], correctIndex: 0},
    {sentence: 'He struck a chord with the audience.', options: ['chord', 'cord'], correctIndex: 0},
    {sentence: 'He started to bawl loudly.', options: ['bawl', 'ball'], correctIndex: 0},
    {sentence: 'My dear friend came to visit.', options: ['dear', 'deer'], correctIndex: 0},
    {sentence: 'She will dye her hair.', options: ['dye', 'die'], correctIndex: 0},
    {sentence: 'Homework is due tomorrow.', options: ['due', 'do'], correctIndex: 0},
    {sentence: 'He wants to ensure it\'s done.', options: ['ensure', 'insure'], correctIndex: 0},
    {sentence: 'The bus fare is expensive.', options: ['fare', 'fair'], correctIndex: 0},
    {sentence: 'She went straight home.', options: ['straight', 'strait'], correctIndex: 0},
    {sentence: 'She is an angel for helping.', options: ['angel', 'angle'], correctIndex: 0},
    {sentence: 'He agreed to a duel.', options: ['duel', 'dual'], correctIndex: 0},
    {sentence: 'Add flour to the mixture.', options: ['flour', 'flower'], correctIndex: 0},
    {sentence: 'The horse had a long mane.', options: ['mane', 'main'], correctIndex: 0},
    {sentence: 'She looks pale.', options: ['pale', 'pail'], correctIndex: 0},
    {sentence: 'He walked past me.', options: ['past', 'passed'], correctIndex: 0},
    {sentence: 'Take a peek at this.', options: ['peek', 'peak'], correctIndex: 0},
    {sentence: 'Shoo the flies away.', options: ['Shoo', 'Shoe'], correctIndex: 0},
    {sentence: 'She bought new stationery.', options: ['stationery', 'stationary'], correctIndex: 0},
    {sentence: 'They erected a statue in the park.', options: ['statue', 'statute'], correctIndex: 0},
    {sentence: 'This is a core tenet of his belief.', options: ['tenet', 'tenant'], correctIndex: 0},
    {sentence: 'Would you help me?', options: ['Would', 'Wood'], correctIndex: 0},
    {sentence: 'He cannot bear this pain.', options: ['bear', 'bare'], correctIndex: 0},
    {sentence: 'She has a flair for design.', options: ['flair', 'flare'], correctIndex: 0},
    {sentence: 'Knead the dough thoroughly.', options: ['Knead', 'Need'], correctIndex: 0},
    {sentence: 'He waived his rights.', options: ['waived', 'waved'], correctIndex: 0},
    {sentence: 'Many women were present.', options: ['women', 'woman'], correctIndex: 0},
    {sentence: 'She has a bright idea.', options: ['bright', 'brite'], correctIndex: 0},
    {sentence: 'He likes to sing songs.', options: ['sing', 'sink'], correctIndex: 0},
    {sentence: 'The dogs are in the pen.', options: ['pen', 'pan'], correctIndex: 0},
    {sentence: 'I have access to the files.', options: ['access', 'excess'], correctIndex: 0},
    {sentence: 'He was standing by the door.', options: ['by', 'buy'], correctIndex: 0},
    {sentence: 'The danger is imminent.', options: ['imminent', 'eminent'], correctIndex: 0},
    {sentence: 'The cat ate its food.', options: ['its', 'it\'s'], correctIndex: 0},
    {sentence: 'Maybe he will come.', options: ['Maybe', 'May'], correctIndex: 0},
    {sentence: 'She adopted a child.', options: ['adopted', 'adapted'], correctIndex: 0},
    {sentence: 'He alluded to the problem.', options: ['alluded', 'eluded'], correctIndex: 0},
    {sentence: 'He apprised me of the situation.', options: ['apprised', 'appraised'], correctIndex: 0},
    {sentence: 'They gave their assent to the plan.', options: ['assent', 'ascent'], correctIndex: 0},
    {sentence: 'He cited a famous study.', options: ['cited', 'sited'], correctIndex: 0},
    {sentence: 'The city council meets today.', options: ['council', 'counsel'], correctIndex: 0},
    {sentence: 'Please be discreet about this.', options: ['discreet', 'discrete'], correctIndex: 0},
    {sentence: 'These drugs are illicit.', options: ['illicit', 'elicit'], correctIndex: 0},
    {sentence: 'She\'s going to college.', options: ['college', 'collage'], correctIndex: 0},
    {sentence: 'He was formerly a chef.', options: ['formerly', 'formally'], correctIndex: 0},
    {sentence: 'He was attacked by a guerrilla.', options: ['guerrilla', 'gorilla'], correctIndex: 0},
    {sentence: 'The team\'s morale was high.', options: ['morale', 'moral'], correctIndex: 0},
    {sentence: 'My diary is on the desk.', options: ['diary', 'dairy'], correctIndex: 0},
    {sentence: 'From my perspective, this is true.', options: ['From', 'Form'], correctIndex: 0},
    {sentence: 'The hiking trail is long.', options: ['trail', 'trial'], correctIndex: 0},
    {sentence: 'His behavior was decent.', options: ['decent', 'descent'], correctIndex: 0},
    {sentence: 'She is the dominant partner.', options: ['dominant', 'dominate'], correctIndex: 0},
    {sentence: 'He tried to exorcise the demon.', options: ['exorcise', 'exercise'], correctIndex: 0},
    {sentence: 'He ate the whole pie.', options: ['whole', 'hole'], correctIndex: 0},
    {sentence: 'The premise of the story is interesting.', options: ['premise', 'premises'], correctIndex: 0},
    {sentence: 'The new residents were friendly.', options: ['residents', 'residence'], correctIndex: 0},
    {sentence: 'He addressed the audience respectfully.', options: ['respectfully', 'respectively'], correctIndex: 0},
    {sentence: 'He drove a stake into the ground.', options: ['stake', 'steak'], correctIndex: 0},
    {sentence: 'He took it apart.', options: ['apart', 'a part'], correctIndex: 0},
    {sentence: 'He used to live here.', options: ['used', 'use'], correctIndex: 0},
    {sentence: 'You are supposed to finish it.', options: ['supposed', 'suppose'], correctIndex: 0},
    {sentence: 'He could have saved her.', options: ['have', 'of'], correctIndex: 0},
    {sentence: 'He barely passed the test.', options: ['barely', 'barley'], correctIndex: 0},
    {sentence: 'He found rice in her hair.', options: ['rice', 'lice'], correctIndex: 0},
    {sentence: 'We are going now.', options: ['are', 'aren\'t'], correctIndex: 0},
    {sentence: 'Isn\'t he nice?', options: ['Isn\'t', 'Is'], correctIndex: 0},
    {sentence: 'She won\'t do that.', options: ['won\'t', 'want'], correctIndex: 0},
    {sentence: 'That isn\'t tall.', options: ['That', 'That\'s'], correctIndex: 0},
    {sentence: 'He changed the world.', options: ['world', 'word'], correctIndex: 0},
    {sentence: 'The country is small.', options: ['country', 'county'], correctIndex: 0},
    {sentence: 'She quit her job.', options: ['quit', 'quiet'], correctIndex: 0},
    {sentence: 'He picked up the pen.', options: ['pen', 'pin'], correctIndex: 0},
    {sentence: 'He bought a pear at the market.', options: ['pear', 'bear'], correctIndex: 0},
    {sentence: 'The dog is barking.', options: ['barking', 'parking'], correctIndex: 0},
    {sentence: 'He called a cab for us.', options: ['cab', 'cap'], correctIndex: 0},
    {sentence: 'Can you swim?', options: ['Can', 'Can\'t'], correctIndex: 0},
  ];

  // Split the quiz data into chunks of 10 questions per set.
  const sets = [];
  for (let i = 0; i < quizData.length; i += 10) {
    sets.push(quizData.slice(i, i + 10));
  }

  // Track user answers. This mirrors the structure of `sets` and
  // stores the index of the option chosen by the user (0 or 1), or
  // null if unanswered.
  const userAnswers = sets.map(set => set.map(() => null));

  // Reference to our root DOM element.
  const app = document.getElementById('app');

  /**
   * Use the Web Speech API to speak text aloud.  If another utterance
   * is currently speaking, it will be cancelled before starting the
   * new one.  We set the language to English and leave the default
   * voice selection to the browser.
   *
   * @param {string} text The text to speak.
   */
  function speak(text) {
    // Cancel any ongoing speech to avoid overlap
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
  }

  /**
   * Render the home screen with a list of quiz sets.  Each button
   * navigates to a different set containing up to 10 questions.
   */
  function showHome() {
    app.innerHTML = '';
    const title = document.createElement('h1');
    title.textContent = 'English Sound Quiz';
    app.appendChild(title);
    const list = document.createElement('div');
    list.className = 'set-list';
    sets.forEach((set, index) => {
      const btn = document.createElement('button');
      btn.textContent = `Set ${index + 1} (${set.length} questions)`;
      btn.addEventListener('click', () => showSet(index));
      list.appendChild(btn);
    });
    app.appendChild(list);
  }

  /**
   * Render a specific set of questions.  Each question is displayed
   * with a button to play the sentence and two option buttons.  Once
   * an option is chosen, the answer is evaluated and both buttons are
   * styled accordingly.  Navigation buttons allow moving between
   * adjacent sets or returning home.
   *
   * @param {number} setIndex The index of the set to display.
   */
  function showSet(setIndex) {
    const set = sets[setIndex];
    app.innerHTML = '';
    const title = document.createElement('h1');
    title.textContent = `Quiz Set ${setIndex + 1}`;
    app.appendChild(title);
    
    // Render each question card
    set.forEach((question, qIndex) => {
      const card = document.createElement('div');
      card.className = 'quiz-card';

      const qTitle = document.createElement('h3');
      qTitle.textContent = `Question ${qIndex + 1}`;
      card.appendChild(qTitle);

      // Play button to hear the sentence
      const playBtn = document.createElement('button');
      playBtn.className = 'play-button';
      playBtn.textContent = 'Play Sentence';
      playBtn.addEventListener('click', () => {
        speak(question.sentence);
      });
      card.appendChild(playBtn);

      // Container for option buttons
      const optionsDiv = document.createElement('div');
      optionsDiv.className = 'option-buttons';

      // Prepare indices array and randomly reverse it to vary the order
      const indices = [0, 1];
      if (Math.random() < 0.5) {
        indices.reverse();
      }
      
      // Create the option buttons
      indices.forEach((optIndex, btnPosition) => {
        const optBtn = document.createElement('button');
        optBtn.className = 'option-btn';
        optBtn.textContent = question.options[optIndex];
        optBtn.addEventListener('click', () => {
          // Prevent re‑answering if already answered
          if (userAnswers[setIndex][qIndex] !== null) return;
          userAnswers[setIndex][qIndex] = optIndex;
          const isCorrect = (optIndex === question.correctIndex);
          // Update styling for each button
          [...optionsDiv.children].forEach((btn, childIdx) => {
            const originalOptIndex = indices[childIdx];
            btn.classList.add('selected');
            if (originalOptIndex === question.correctIndex) {
              btn.classList.add('correct');
            } else if (childIdx === btnPosition) {
              btn.classList.add('wrong');
            }
            btn.disabled = true;
          });
          // Display the result message
          resultDiv.textContent = isCorrect ? 'correct :)' : 'wrong :(';
          resultDiv.style.color = isCorrect ? '#155724' : '#721c24';
        });
        optionsDiv.appendChild(optBtn);
      });
      card.appendChild(optionsDiv);

      // Placeholder for result message
      const resultDiv = document.createElement('div');
      resultDiv.className = 'result-msg';
      card.appendChild(resultDiv);

      app.appendChild(card);
    });

    // Navigation controls
    const nav = document.createElement('div');
    nav.className = 'navigation';
    
    const backBtn = document.createElement('button');
    backBtn.className = 'nav-btn';
    backBtn.textContent = 'Back';
    backBtn.disabled = (setIndex === 0);
    backBtn.addEventListener('click', () => {
      if (setIndex > 0) {
        showSet(setIndex - 1);
      }
    });
    nav.appendChild(backBtn);

    const homeBtn = document.createElement('button');
    homeBtn.className = 'nav-btn primary';
    homeBtn.textContent = 'Home';
    homeBtn.addEventListener('click', () => showHome());
    nav.appendChild(homeBtn);

    const nextBtn = document.createElement('button');
    nextBtn.className = 'nav-btn';
    nextBtn.textContent = 'Next';
    nextBtn.disabled = (setIndex >= sets.length - 1);
    nextBtn.addEventListener('click', () => {
      if (setIndex < sets.length - 1) {
        showSet(setIndex + 1);
      }
    });
    nav.appendChild(nextBtn);

    app.appendChild(nav);
  }

  // Kick off the application
  showHome();
})();
