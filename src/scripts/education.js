/* eslint-disable */
document.querySelectorAll(".tna-filters").forEach(($filters) => {
  $filters.querySelectorAll(".tna-filters__item").forEach(($item) => {
    const $toggleButton = $item.querySelector(".tna-filters__button");
    const $toggleButtonText =
      $toggleButton && $toggleButton.querySelector(".tna-filters__button-text");
    const $content = $item.querySelector(".tna-filters__content");
    if (!$toggleButton || !$toggleButtonText || !$content) {
      return;
    }
    let isExpanded = $toggleButton.getAttribute("aria-expanded") === "true";
    const update = () => {
      $toggleButton.setAttribute("aria-expanded", isExpanded.toString());
      if (isExpanded) {
        $content.removeAttribute("hidden");
        $toggleButtonText.textContent = "Hide";
      } else {
        $content.setAttribute("hidden", "");
        $toggleButtonText.textContent = "Show";
      }
    };
    const toggle = () => {
      isExpanded = !isExpanded;
      update();
    };
    $toggleButton.removeAttribute("hidden");
    $toggleButton.addEventListener("click", () => {
      toggle();
    });
    update();
  });
});

if (
  window.Worker &&
  window.Blob &&
  window.URL &&
  window.TextEncoder &&
  window.CompressionStream
) {
  /**
   * Main function to generate a ZIP Blob from an array of Blob files.
   * @param {Array<{name: string, blob: Blob}>} fileList
   * @returns {Promise<Blob>}
   */
  const createZipFromBlobs = async function (fileList) {
    // Inline Web Worker Code
    const workerCode = `
    // CRC-32 Lookup Table for fast streaming calculations
    const crcTable = new Uint32Array(256);
    for (let i = 0; i < 256; i++) {
      let c = i;
      for (let j = 0; j < 8; j++) {
        c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      }
      crcTable[i] = c;
    }

    self.onmessage = async (e) => {
      const files = e.data; // [{ name, blob }]
      const chunks = [];
      const centralDirectoryEntries = [];
      let offset = 0;

      for (const file of files) {
        const nameBytes = new TextEncoder().encode(file.name);
        const uncompressedSize = file.blob.size;

        // 1. Calculate CRC-32 by reading the blob in chunks
        let crc = 0xFFFFFFFF;
        const reader = file.blob.stream().getReader();
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          for (let i = 0; i < value.length; i++) {
            crc = (crc >>> 8) ^ crcTable[(crc ^ value[i]) & 0xFF];
          }
        }
        const checksum = (crc ^ 0xFFFFFFFF) >>> 0;

        // 2. Compress the blob stream using raw DEFLATE
        const compressedStream = file.blob.stream().pipeThrough(new CompressionStream('deflate-raw'));
        const compressedChunks = [];
        const compReader = compressedStream.getReader();
        
        while (true) {
          const { done, value } = await compReader.read();
          if (done) break;
          compressedChunks.push(value);
        }

        const compressedSize = compressedChunks.reduce((acc, c) => acc + c.byteLength, 0);

        // 3. Construct Local Header (30 bytes + name length)
        const localHeader = new Uint8Array(30 + nameBytes.length);
        const lhView = new DataView(localHeader.buffer);

        lhView.setUint32(0, 0x04034b50, true); // Local header signature
        lhView.setUint16(4, 20, true);         // Version needed (2.0)
        lhView.setUint16(6, 0, true);          // General bit flag
        lhView.setUint16(8, 8, true);          // Compression method (8 = Deflate)
        lhView.setUint16(10, 0, true);         // Last mod time
        lhView.setUint16(12, 0, true);         // Last mod date
        lhView.setUint32(14, checksum, true);  // CRC-32
        lhView.setUint32(18, compressedSize, true);
        lhView.setUint32(22, uncompressedSize, true);
        lhView.setUint16(26, nameBytes.length, true);
        lhView.setUint16(28, 0, true);
        localHeader.set(nameBytes, 30);

        // Track entry for the Central Directory at the end
        centralDirectoryEntries.push({
          nameBytes,
          checksum,
          compressedSize,
          uncompressedSize,
          offset
        });

        chunks.push(localHeader);
        offset += localHeader.byteLength;

        for (const chunk of compressedChunks) {
          chunks.push(chunk);
          offset += chunk.byteLength;
        }
      }

      // 4. Construct Central Directory
      const cdOffset = offset;
      let cdSize = 0;

      for (const entry of centralDirectoryEntries) {
        const cdHeader = new Uint8Array(46 + entry.nameBytes.length);
        const cdView = new DataView(cdHeader.buffer);

        cdView.setUint32(0, 0x02014b50, true); // Central directory signature
        cdView.setUint16(4, 20, true);         // Version made by
        cdView.setUint16(6, 20, true);         // Version needed
        cdView.setUint16(8, 0, true);          // General bit flag
        cdView.setUint16(10, 8, true);         // Compression method (Deflate)
        cdView.setUint16(12, 0, true);        // Mod time
        cdView.setUint16(14, 0, true);        // Mod date
        cdView.setUint32(16, entry.checksum, true);
        cdView.setUint32(20, entry.compressedSize, true);
        cdView.setUint32(24, entry.uncompressedSize, true);
        cdView.setUint16(28, entry.nameBytes.length, true);
        cdView.setUint16(30, 0, true);
        cdView.setUint16(32, 0, true);
        cdView.setUint16(34, 0, true);
        cdView.setUint32(38, 0, true);
        cdView.setUint32(42, entry.offset, true);
        cdHeader.set(entry.nameBytes, 46);

        chunks.push(cdHeader);
        cdSize += cdHeader.byteLength;
      }

      // 5. Construct End of Central Directory Record (EOCD)
      const eocd = new Uint8Array(22);
      const eocdView = new DataView(eocd.buffer);

      eocdView.setUint32(0, 0x06054b50, true);
      eocdView.setUint16(4, 0, true);
      eocdView.setUint16(6, 0, true);
      eocdView.setUint16(8, centralDirectoryEntries.length, true);
      eocdView.setUint16(10, centralDirectoryEntries.length, true);
      eocdView.setUint32(12, cdSize, true);
      eocdView.setUint32(16, cdOffset, true);
      eocdView.setUint16(20, 0, true);

      chunks.push(eocd);

      // Return final ZIP Blob
      const zipBlob = new Blob(chunks, { type: 'application/zip' });
      self.postMessage(zipBlob);
    };
  `;

    // Spawn Web Worker using a Blob URL
    const workerBlob = new Blob([workerCode], {
      type: "application/javascript",
    });
    const workerUrl = URL.createObjectURL(workerBlob);
    const worker = new Worker(workerUrl);

    return new Promise((resolve, reject) => {
      worker.onmessage = (e) => {
        URL.revokeObjectURL(workerUrl);
        worker.terminate();
        resolve(e.data); // Returns the ZIP Blob
      };

      worker.onerror = (err) => {
        URL.revokeObjectURL(workerUrl);
        worker.terminate();
        reject(err);
      };

      // Blobs can be passed directly via postMessage without needing transferables
      worker.postMessage(fileList);
    });
  };

  const $downloadBlock = document.getElementById("download");
  const $downloadButton = document.getElementById("download-sources");
  const $downloadError = document.getElementById("download-error");

  if ($downloadBlock && $downloadButton && $downloadError) {
    const $sidebarItem = document.querySelector(
      ".tna-sidebar__item[hidden]:has(a[href='#download'])",
    );
    if ($sidebarItem) {
      $sidebarItem.removeAttribute("hidden");
    }

    $downloadBlock.removeAttribute("hidden");

    const originalButtonText = $downloadButton.textContent;
    const originalButtonIcon = $downloadButton
      .querySelector("i")
      .cloneNode(true);

    const reEnableButton = (options) => {
      const { text } = options;
      $downloadButton.removeAttribute("disabled");
      $downloadButton.textContent = text;
      $downloadButton.prepend(originalButtonIcon.cloneNode(true));
    };

    $downloadButton.addEventListener("click", async () => {
      $downloadButton.blur();
      $downloadButton.setAttribute("disabled", "true");
      $downloadError.setAttribute("hidden", "hidden");
      $downloadButton.textContent = "Downloading...";

      const files = await fetch("?sources")
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .catch((error) => {
          reEnableButton({ text: originalButtonText });
          $downloadError.textContent =
            "Error: There was a problem downloading the list of files. Try again later.";
          $downloadError.removeAttribute("hidden");
          $downloadError.focus();
        });

      const fileBlobs = await Promise.all(
        files.map(async (file) => {
          const response = await fetch(file.source);
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return { name: file.target, blob: await response.blob() };
        }),
      ).catch((error) => {
        reEnableButton({ text: originalButtonText });
        $downloadError.textContent =
          "Error: There was a problem downloading the files. Try again later.";
        $downloadError.removeAttribute("hidden");
        $downloadError.focus();
      });

      try {
        const zipBlob = await createZipFromBlobs(fileBlobs);
        const downloadLink = document.createElement("a");
        downloadLink.href = URL.createObjectURL(zipBlob);
        downloadLink.download = `${$downloadButton.dataset.fileName}`;
        downloadLink.click();
      } catch (error) {
        reEnableButton({ text: originalButtonText });
        $downloadError.removeAttribute("hidden");
        $downloadError.textContent =
          "Error: There was a problem creating the ZIP file. Try again later.";
        $downloadError.focus();
      }

      $downloadButton.removeAttribute("disabled");
      $downloadButton.textContent = "Download complete";
      const downloadedButtonIcon = document.createElement("i");
      downloadedButtonIcon.classList.add("fa-solid", "fa-check");
      downloadedButtonIcon.setAttribute("aria-hidden", "true");
      $downloadButton.prepend(downloadedButtonIcon);
      $downloadButton.focus();
    });

    $downloadButton.addEventListener("blur", async () => {
      reEnableButton({ text: originalButtonText });
    });
  }
}
