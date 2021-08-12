# Weekly To Do List

*please add each week's tasks to the top of this document*

## August 6th - August 13th

Jacques Laroche:

- [ ] Look up how to train Keras networks on arrays of different sizes

- [ ] [WORKED ON] Grow the Anthems Dataset
   Look up getting Midi files from MuseScore (reference: https://www.tech-gate.org/usa/2021/07/21/audacitys-new-owner-is-in-another-fight-with-the-open-source-community/)
   Status: 
    I've identified what Genre and files we could use for training. I then tried to use the Github tools to bulk download Midi files from the MuseScore site that we could use for training. Unfortunately, the tools seem to be a bit lacking and I'm talking to the developer (Xmader) on the project's Discord schannel to see what possible ways forward there are for us.

- [ ] [WORKED ON] Look up other ML projects related to the Anthems project and take note of their approach
   Status:
    Found an article about using audio instead of images as the dataset for a GAN. Link to the piece is below. 
    https://towardsdatascience.com/synthesizing-audio-with-generative-adversarial-networks-8e0308184edd
	NOTE: This article got me thinking that maybe we are thinking about things wrong when it comes to using SVGs instead of raster images. SPecifically, perhaps we should be analyzing the SVGs with an NLP algorithm since we are actually dealing with text rather than an image (in the traditional sense).
   
- [ ] Go through code and add comments

- [x] Add a weekly tasks document and add to Github --> inform team

Antonije Petrovic:

- [ ] [WORKED ON] Research about LSTM Autoencoders.
    Status: Tried different basic examples, but nothing too interesting for now.
- [ ] Research about RNNs.
- [ ] [WORKED ON] Consider more ways of SVG feature representation.
    Status: Found yet another way for svg2vector representation. Added a link to the article to our Google Doc. Will research more about this. Maybe we will end up trying out different approaches and in the end we'll see what works best.