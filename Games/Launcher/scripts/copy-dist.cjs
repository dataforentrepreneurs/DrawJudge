const fs = require('fs');
const path = require('path');

function copyRecursiveSync(src, dest) {
    if (!fs.existsSync(src)) {
        console.log(`Source directory not found: ${src}. Skipping copy.`);
        return;
    }

    const exists = fs.existsSync(src);
    const stats = exists && fs.statSync(src);
    const isDirectory = exists && stats.isDirectory();

    if (isDirectory) {
        if (!fs.existsSync(dest)) {
            fs.mkdirSync(dest, { recursive: true });
        }
        fs.readdirSync(src).forEach(function(childItemName) {
            copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
        });
    } else {
        fs.copyFileSync(src, dest);
    }
}

function copyGame(gameName) {
    const src = path.join(__dirname, `../../${gameName}/dist`);
    const dest = path.join(__dirname, `../dist/${gameName.toLowerCase()}`);
    console.log(`Copying ${gameName} from ${src} to ${dest}`);
    copyRecursiveSync(src, dest);
}

console.log(`Starting cross-platform copy dist...`);

try {
    copyGame('DrawJudge');
    copyGame('CoupleClash');
    console.log('Successfully copied game dists to Launcher dist.');
} catch (err) {
    console.error('Error during cross-platform copy:', err);
    // On Render, we don't want to crash the whole build if this optional local step fails
    if (process.env.RENDER) {
        process.exit(0);
    } else {
        process.exit(1);
    }
}
