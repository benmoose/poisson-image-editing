export default {
  t1: {
    number: 1,
    desc: `
      Select a grayscale image. Mark out a region using a polygon (you can use rpoly).
      Remove the selected region and fill it in using the Equation (2) in the paper.
      You are solving for unknown intensity values inside the region R.
      Test the method in smooth regions and also in regions with edges (high-frequency).
      Also report the behavior as the size of the selected region increases.
    `
  },
  t2: {
    number: 2,
    desc: `
    Now we are ready to try ‘seamless cloning’. The relevant Equations are (9) to (11).
    Perform both versions (a) importing gradients and (b) mixing gradients.
    `
  },
  t3: {
    number: 3,
    desc: `
      Repeat task 2(a) for color images.
      You have to process R, G, B components separately.
    `
  },
  t4: {
    number: 4,
    desc: `
      Select images you like to edit and show interesting effects.
      Try to record the intermediate results; you can allow multiple strokes in
      this stage. Try to create some ‘cool’ effects.
    `
  },
  t5: {
    number: 5,
    desc: `
      Implement only one of the selection editing effects described in Section 4
      of the paper. You can decide between: texture flattening, local illumination
      changes, local colour changes or seamless tiling.
    `
  }
}
